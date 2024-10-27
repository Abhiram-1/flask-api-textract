from config.aws_config import get_textract_client
from trp import Document
import re

# Define required fields with variations
REQUIRED_FIELDS = {
    "Place of Delivery": ["PLACE OF DELIVERY", "FINAL DESTINATION", "DESTINATION", "PORT OF DISCHARGE"],
    "Shipper Name, Address & Reference code": ["SHIPPER", "BOOKING REF", "CUSTOMS REFERENCE", "OUR REFERENCE"],
    "Consignee Name and Address": ["CONSIGNEE", "RECEIVER"],
    "Notify Party": ["NOTIFY", "NOTIFY PARTY"],
    "Delivery Agent": ["DELIVERY AGENT", "AGENT"],
    "Place of Receipt / POL": ["PLACE OF RECEIPT", "PORT OF LOADING", "POL"],
    "Place of Delivery / POD": ["PORT OF DISCHARGE", "POD"],
    "BL Type - Express / Original": ["NUMBER OF ORIGINAL BILLS", "BILLS OF LADING", "BL TYPE"],
    "Marks & Nos": ["MARKS & NUMBERS", "CONTAINER/TRAILER NO MARKS"],
    "Number of Package and type of packaging": ["PACKAGES", "TOTAL OF CONSIGNMENT"],
    "HS CODE": ["HS CODE"],
    "Goods Description": ["DESCRIPTION OF GOODS", "GOODS DESCRIPTION"],
    "Weight": ["GROSS(KG)", "WEIGHT"],
    "Volume": ["CUBE(M3)", "VOLUME"]
}

def analyze_pdf(document_bytes):
    textract = get_textract_client()
    try:
        response = textract.analyze_document(
            Document={'Bytes': document_bytes},
            FeatureTypes=['FORMS', 'TABLES', 'LAYOUT']
        )
        return response
    except Exception as e:
        print("Textract Error:", e)
        raise

def extract_fields(response):
    # Initialize all fields to "Not Found"
    extracted_data = {field: "Not Found" for field in REQUIRED_FIELDS.keys()}
    doc = Document(response)

    # 1. Extract key-value pairs from form fields
    for page in doc.pages:
        for field in page.form.fields:
            if field.key and field.value:
                key_text = field.key.text.strip().upper()
                value_text = field.value.text.strip()
                for req_field, variations in REQUIRED_FIELDS.items():
                    if any(var.upper() in key_text for var in variations):
                        extracted_data[req_field] = value_text
                        print(f"Form Extraction: {req_field} -> {value_text}")

        # 2. Enhanced Table Extraction with Row Concatenation
        for table in page.tables:
            current_field = None
            for row in table.rows:
                if len(row.cells) < 2:
                    continue

                # Extract potential key and values
                key_text = row.cells[0].text.strip().upper()
                value_text = ' '.join([cell.text.strip() for cell in row.cells[1:]])

                for req_field, variations in REQUIRED_FIELDS.items():
                    if any(var.upper() in key_text for var in variations):
                        # Check if key_text includes a colon
                        if ":" in key_text:
                            key_text_split = key_text.split(":")
                            if len(key_text_split) > 1:
                                value_text = key_text_split[1].strip() + " " + value_text
                        
                        # Concatenate multiline data for the same field
                        if extracted_data[req_field] == "Not Found":
                            extracted_data[req_field] = value_text
                        else:
                            extracted_data[req_field] += " " + value_text
                        current_field = req_field
                        break

                # Append multiline entries if current_field is set
                if current_field and not any(var.upper() in key_text for var in REQUIRED_FIELDS[current_field]):
                    extracted_data[current_field] += " " + value_text
                    print(f"Multiline Table Entry for {current_field} -> {extracted_data[current_field]}")

    # 3. Query Extraction for Remaining Fields
    queries = []
    for field, variations in REQUIRED_FIELDS.items():
        if extracted_data[field] == "Not Found":
            queries.append({
                'Text': f"What is the {variations[0]}?",
                'Alias': field
            })

    if queries:
        try:
            textract_client = get_textract_client()
            query_response = textract_client.analyze_document(
                Document={'Bytes': response['Document']['Bytes']},
                FeatureTypes=['QUERIES'],
                QueriesConfig={'Queries': queries[:30]}
            )
            for block in query_response['Blocks']:
                if block['BlockType'] == 'QUERY_RESULT' and block.get('Text'):
                    alias = block['Query']['Alias']
                    if alias in extracted_data and extracted_data[alias] == "Not Found":
                        extracted_data[alias] = block['Text']
                        print(f"Query Extraction: {alias} -> {block['Text']}")
        except Exception as e:
            print(f"Query extraction error: {e}")

    # 4. Regex Fallback Extraction for Specific Fields
    document_text = "\n".join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])
    regex_patterns = {
        "HS CODE": re.compile(r'HS CODE\s*([0-9]+)'),
        "Weight": re.compile(r'GROSS\(KG\)\s*([0-9,]+)'),
        "Volume": re.compile(r'CUBE\(M3\)\s*([0-9.]+)')
    }

    for field, pattern in regex_patterns.items():
        if extracted_data[field] == "Not Found":
            match = pattern.search(document_text)
            if match:
                extracted_data[field] = match.group(1).strip()
                print(f"Regex Extraction: {field} -> {extracted_data[field]}")

    return extracted_data

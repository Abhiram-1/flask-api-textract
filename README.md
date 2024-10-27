# Textract PDF Data Extraction API 📄

A robust AWS Textract-based solution for extracting structured data from cargo invoice PDFs. This API leverages Textract's advanced features (FORMS, TABLES, LAYOUT, and QUERIES) to accurately capture essential fields like "Place of Delivery," "Shipper," "Consignee," and more.

## 🚀 Features

- **Intelligent Data Extraction**
  - Form field detection
  - Table structure recognition
  - Layout analysis



## 🛠️ Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd textract_project
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS Credentials**
   - Ensure AWS credentials are properly configured
   - Set up necessary IAM permissions for Textract

4. **Run the Application**
   ```bash
   python app.py
   ```

## 🔌 API Usage

### Extract Data Endpoint

**Endpoint:** `/extract`  
**Method:** `POST`  
**Content-Type:** `multipart/form-data`

#### Request
```http
POST /extract
Content-Type: multipart/form-data
```

#### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| file | File | PDF document to process |

#### Sample Response
```json
{
  "shipper": "Example Shipping Co.",
  "consignee": "Sample Receiver Ltd.",
  "placeOfDelivery": "Port of Example",
  "status": "success"
}
```



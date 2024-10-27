# textract_project/app.py
from flask import Flask, request, jsonify
from textract_processor import analyze_pdf, extract_fields

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Textract PDF Data Extraction API. Use the '/extract' endpoint to upload a PDF file for extraction."

@app.route('/extract', methods=['POST'])
def extract_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    pdf_file = request.files['file']
    document_bytes = pdf_file.read()
    
    response = analyze_pdf(document_bytes)
    extracted_data = extract_fields(response)
    
    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)

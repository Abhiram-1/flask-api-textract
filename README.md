Textract PDF Data Extraction API

This project uses AWS Textract to extract structured data from PDF documents, specifically designed to handle cargo invoice bills. By leveraging Textract's FORMS, TABLES, LAYOUT, and QUERIES features, this application accurately captures fields such as "Place of Delivery," "Shipper," "Consignee," and more.

Table of Contents

Project Overview
Features
Setup and Installation
API Usage
Deploying on AWS Lambda
Project Overview
The Textract PDF Data Extraction API processes PDF invoices to extract relevant information and present it in structured JSON format. It uses:

AWS Textract for optical character recognition (OCR) and layout analysis.
Flask for API development, enabling easy integration with other services or applications.
Lambda and API Gateway for serverless deployment (optional).
Features
Data Extraction: Extracts key-value pairs, table data, and layout information for invoices.
Enhanced Extraction Techniques:
Colon Handling: Detects fields with a colon (e.g., "Shipper :") and extracts the value that follows.
Row Concatenation: Combines multi-line and multi-cell data.
Regex Patterns: Uses regex as a fallback for fields not captured through form or table analysis.
Query Extraction: Fills in missing fields by directly asking Textract for specific data points.
Setup and Installation
Clone the Repository:
bash
Copy code
git clone <your-repository-url>
cd textract_project
Install Required Dependencies:
bash
Copy code
pip install -r requirements.txt
Add AWS Credentials: Ensure your AWS credentials are set up in your environment or AWS CLI, as Textract requires authentication.
Run the Flask API:
bash
Copy code
python app.py
The server will run locally at http://127.0.0.1:5000.
API Usage
Endpoint: /extract

Method: POST
Description: Upload a PDF file to extract data fields.
Request Parameters

file: A PDF file to be uploaded as form-data.
Sample Request (using Postman or similar)

Set the URL to http://127.0.0.1:5000/extract.
Choose POST method.
In form-data, add a key file and select a PDF file to upload.

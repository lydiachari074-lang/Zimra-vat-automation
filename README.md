\# 🇿🇼 ZIMRA VAT Return Automation

&#x20;   

&#x20;   A Streamlit web app that automates VAT calculation for ZIMRA in Zimbabwe.

&#x20;   

&#x20;   ## Features

&#x20;   - Upload CSV/Excel of sales and purchases

&#x20;   - Automatically calculates Output Tax, Input Tax, Net VAT Payable

&#x20;   - Generates Audit Trail with VAT per transaction

&#x20;   - Downloadable VAT Return Excel for ZIMRA submission

&#x20;   

&#x20;   ## How to Run Locally

&#x20;   1. Install requirements: `pip install -r requirements.txt`

&#x20;   2. Run app: `streamlit run ai.py`

&#x20;   

&#x20;   ## Sample File Format

&#x20;   Required columns: `date, type, description, amount, supply\_type, vat\_rate`

&#x20;   `type` must be `sale` or `purchase`. `vat\_rate` is 0.15 for 15%


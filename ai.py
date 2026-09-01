import streamlit as st
import pandas as pd

st.title("ZW ZIMRA VAT Return Automation")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # 1. Read the file
    df = pd.read_csv(uploaded_file)
    
    # 2. CLEAN COLUMN NAMES - THIS IS THE FIX
    df.columns = df.columns.str.lower().str.strip() # make everything lowercase: "Description" -> "description"
    
    # 3. RENAME to match what our code uses
    df = df.rename(columns={
        'taxable_amount': 'amount',  # your csv has this, code needs 'amount'
        'type': 'type',
        'description': 'description',
        'supply_type': 'supply_type',
        'vat_rate': 'vat_rate',
        'date': 'date'
    })
    
    st.subheader("1. Raw Data Preview")
    st.dataframe(df)
    
    # 4. CALCULATE VAT - Now it won't crash
    if st.button("Calculate VAT"):
        
        # Make sure amount and vat_rate are numbers
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['vat_rate'] = pd.to_numeric(df['vat_rate'], errors='coerce')
        
        # Calculate VAT for each row
        df['vat'] = df['amount'] * df['vat_rate']
        
        # Output VAT = Sales
        output_vat = df[df['type'].str.lower() == 'sale']['vat'].sum()
        
        # Input VAT = Purchases
        input_vat = df[df['type'].str.lower() == 'purchase']['vat'].sum()
        
        # VAT Payable
        vat_payable = output_vat - input_vat
        
        st.subheader("2. VAT Summary")
        st.metric("Output VAT", f"${output_vat:,.2f}")
        st.metric("Input VAT", f"${input_vat:,.2f}")
        st.metric("VAT Payable / Refundable", f"${vat_payable:,.2f}")

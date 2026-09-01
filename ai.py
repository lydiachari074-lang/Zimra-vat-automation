import streamlit as st
import pandas as pd

st.title("ZW ZIMRA VAT Return Automation")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # FIX 1: Clean column names. "Amount" -> "amount", "Taxable_Amount" -> "taxable_amount"
    df.columns = df.columns.str.lower().str.strip()
    
    # FIX 2: Auto-detect the amount column
    amount_col = None
    for col in ['amount', 'taxable_amount', 'value']:
        if col in df.columns:
            amount_col = col
            break
    
    if amount_col is None:
        st.error("Error: Could not find an 'amount' or 'taxable_amount' column in your CSV")
        st.stop()
    
    # FIX 3: Rename it to 'amount' so the rest of the code works
    df = df.rename(columns={amount_col: 'amount'})
    
    st.subheader("1. Raw Data Preview")
    st.dataframe(df)
    
    if st.button("Calculate VAT"):
        
        # Make sure columns are numbers
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

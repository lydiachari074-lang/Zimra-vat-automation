import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="ZIMRA VAT Return Automation", layout="wide")
st.title("🇿🇼 ZIMRA VAT Return Automation")

uploaded_file = st.file_uploader("Upload your transactions CSV or Excel", type=["csv", "xlsx"])

def calculate_vat(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['vat_amount'] = df['amount'] * df['vat_rate']
    output_tax = df[df['type'] == 'sale']['vat_amount'].sum()
    input_tax = df[df['type'] == 'purchase']['vat_amount'].sum()
    net_vat = output_tax - input_tax
    return df, output_tax, input_tax, net_vat

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("File Uploaded Successfully!")
    st.subheader("1. Raw Data Preview")
    st.dataframe(df, use_container_width=True)

    if st.button("🧮 Calculate VAT Return", type="primary"):
        audit_df, output_tax, input_tax, net_vat = calculate_vat(df)
        
        st.subheader("2. VAT Calculation Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Output Tax", f"${output_tax:,.2f}")
        col2.metric("Input Tax", f"${input_tax:,.2f}")
        col3.metric("Net VAT Payable", f"${net_vat:,.2f}", delta_color="inverse")

        st.subheader("3. Audit Trail")
        st.dataframe(audit_df, use_container_width=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            audit_df.to_excel(writer, sheet_name='Audit_Trail', index=False)
            summary_df = pd.DataFrame({'Description': ['Total Output Tax', 'Total Input Tax', 'Net VAT Payable'],'Amount': [output_tax, input_tax, net_vat]})
            summary_df.to_excel(writer, sheet_name='VAT_Summary', index=False)
        
        st.download_button("📥 Download VAT Return for ZIMRA", data=output.getvalue(), file_name="ZIMRA_VAT_Return.xlsx")
else:
    st.info("Required columns: date, type, description, amount, supply_type, vat_rate")
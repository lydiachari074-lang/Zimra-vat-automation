import pandas as pd
import streamlit as st

st.title("ZIMRA VAT Return Automation")

# Load default file
df = pd.read_csv("sample_august.csv", encoding='utf-8')

# --- NEW: CALCULATE TOTALS ---
total_sales = df[df['type'] == 'sale']['amount'].sum()
total_purchases = df[df['type'] == 'purchase']['amount'].sum()
total_transactions = len(df)

# Calculate VAT
output_vat = df[(df['type'] == 'sale') & (df['supply_type'] == 'Standard')]['amount'].sum() * 0.15
input_vat = df[(df['type'] == 'purchase') & (df['supply_type'] == 'Standard')]['amount'].sum() * 0.15
vat_payable = output_vat - input_vat
# --- END NEW ---

# --- NEW: SHOW TOTALS AT TOP ---
st.subheader("1. Summary Totals")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Purchases", f"${total_purchases:,.2f}")
col3.metric("Total Transactions", f"{total_transactions}")
# --- END NEW ---

st.subheader("2. VAT Summary")
st.write(f"**Output VAT:** ${output_vat:,.2f}")
st.write(f"**Input VAT:** ${input_vat:,.2f}")
st.write(f"**VAT Payable:** ${vat_payable:,.2f}")

st.subheader("3. Transaction Data")
st.dataframe(df)

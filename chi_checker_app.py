
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CHI Drug Checker", layout="centered")

st.title("CHI Drug Compatibility Checker")

# Upload Excel file
uploaded_file = st.file_uploader("Upload CHI Drug Formulary Excel File", type=["xlsx"])

if uploaded_file:
    try:
        # Load the Excel sheet, skipping first 4 rows to get real headers
        df = pd.read_excel(uploaded_file, skiprows=4)

        # Clean up column names
        df.columns = df.columns.str.strip()

        # Check necessary columns
        required_cols = ["SCIENTIFIC NAME", "DESCRIPTION CODE 
(ACTIVE INGREDIENT- STRENGTH-PHARMACEUTICAL FORM)",
                         "ICD 10 CODE", "INDICATION"]
        if not all(col in df.columns for col in required_cols):
            st.error("Excel file is missing one or more required columns.")
        else:
            # Input section
            drug_input = st.text_input("Enter Drug Scientific Name:")
            diagnosis_input = st.text_input("Enter Diagnosis or ICD 10 Code:")

            if st.button("Check Compatibility"):
                matches = df[
                    df["SCIENTIFIC NAME"].str.contains(drug_input, case=False, na=False) &
                    (df["ICD 10 CODE"].astype(str).str.contains(diagnosis_input, case=False, na=False) |
                     df["INDICATION"].str.contains(diagnosis_input, case=False, na=False))
                ]

                if not matches.empty:
                    st.success(f"Match found! {len(matches)} record(s) compatible:")
                    st.dataframe(matches[required_cols])
                else:
                    st.warning("No compatible drug found for this diagnosis.")
    except Exception as e:
        st.error(f"Failed to load Excel: {e}")

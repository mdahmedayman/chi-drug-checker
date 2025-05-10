import streamlit as st
import pandas as pd

st.set_page_config(page_title="CHI Drug Compatibility Checker", layout="wide")
st.title("CHI Drug Compatibility Checker")

# Upload Excel file
uploaded_file = st.file_uploader("Upload CHI Drug Formulary Excel File", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df['Scientific Name'] = df['Scientific Name'].str.lower()
        df['Indication'] = df['Indication'].astype(str).str.lower()
        df['ICD10 Code'] = df['ICD10 Code'].astype(str).str.upper()
        st.success("Excel file loaded successfully!")

        # Input fields
        drug_name = st.text_input("Enter Drug Name (e.g. amoxicillin)").lower()
        diagnosis = st.text_input("Enter Diagnosis or ICD-10 Code (e.g. J01 or sinusitis)").lower()

        if st.button("Check Compatibility"):
            filtered = df[df['Scientific Name'].str.contains(drug_name, na=False)]
            result = filtered[
                filtered['ICD10 Code'].str.contains(diagnosis.upper(), na=False) |
                filtered['Indication'].str.contains(diagnosis, na=False)
            ]

            if not result.empty:
                st.write(f"### {len(result)} Result(s) Found:")
                st.dataframe(result[['Scientific Name', 'Description Code', 'ICD10 Code', 'Indication']])
            else:
                st.warning("No compatible match found.")
    except Exception as e:
        st.error(f"Failed to load Excel: {e}")
else:
    st.info("Please upload the CHI Drug Formulary Excel file to begin.")
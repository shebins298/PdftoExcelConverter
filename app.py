# app.py
import streamlit as st
import PyPDF2
from docx import Document
import tabula
import pandas as pd
import os

# Required system setup (run once)
def setup():
    st.write("Installing dependencies...")
    os.system('apt-get install -y openjdk-8-jdk-headless')
    os.system('pip install PyPDF2 tabula-py python-docx pandas openpyxl streamlit')

def pdf_to_word(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    doc = Document()
    doc.add_paragraph(text)
    doc.save('output.docx')
    return 'output.docx'

def pdf_to_excel(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with pd.ExcelWriter('output.xlsx') as writer:
        for i, table in enumerate(tables):
            table.to_excel(writer, sheet_name=f'Table {i+1}', index=False)
        text_df = pd.DataFrame([text], columns=['Extracted Text'])
        text_df.to_excel(writer, sheet_name='Text Content', index=False)
    
    return 'output.xlsx'

# Streamlit UI
st.title("PDF Converter App 📄➡️📊")
st.markdown("Convert PDFs to Word documents or Excel spreadsheets")

uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    format_choice = st.radio("Select output format:", 
                           ("Word Document", "Excel Spreadsheet"))
    
    if st.button("Convert"):
        try:
            with st.spinner("Converting..."):
                if format_choice == "Word Document":
                    output_file = pdf_to_word("temp.pdf")
                else:
                    output_file = pdf_to_excel("temp.pdf")
            
            st.success("Conversion complete!")
            
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Converted File",
                    data=f,
                    file_name=output_file,
                    mime="application/octet-stream"
                )
            
            # Cleanup
            os.remove("temp.pdf")
            os.remove(output_file)
        
        except Exception as e:
            st.error(f"Error during conversion: {str(e)}")

# setup()  # Uncomment this line if running for the first time

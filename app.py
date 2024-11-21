
import streamlit as st
import PyPDF2
import google.generativeai as genai
import os
import pandas as pd

st.set_page_config(page_title="Automated Resume Analyzer", layout="wide")

if "results_df" not in st.session_state:
    st.session_state.results_df = pd.DataFrame(columns=["Name", "CGPA", "Top Area of Interest", "Main Achievement", "Top Personal Skill", "Location"])

def extract_pdf_information(pdf_file):
    resume_info = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            lines = page.extract_text().split('\n')
            resume_info += (" ".join(lines)) + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return resume_info

def matcher(content, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        st.error(f"Error with AI generation: {e}")
        return ""

st.title("Automated Resume Analyzer")
st.markdown(
    """
    Upload your PDF resumes to extract and analyze their content. 
    """
)

api_key = "AIzaSyDm8WVyu5FO4DYc5-OZAWKPC5MjHZ5AMdg" 

uploaded_files = st.file_uploader("Upload PDF Files", type="pdf", accept_multiple_files=True)

if uploaded_files and api_key:
    st.success("Processing files...")

    for uploaded_file in uploaded_files:
        st.subheader(f"Processing: {uploaded_file.name}")
        
        resume_content = extract_pdf_information(uploaded_file)
        st.text_area("Extracted Content", resume_content, height=200)

        query = (
            resume_content
            + "Provide as a comma-separated text: the CGPA, top area of interest, main achievement, top personal skill, and location."
        )
        result = matcher(query, api_key)

        st.markdown("### AI Analysis Results")
        st.write(result)

        result_data = result.split(",")
        if len(result_data) == 5:
            st.session_state.results_df.loc[len(st.session_state.results_df)] = [uploaded_file.name] + result_data

    st.sidebar.markdown("### Analysis Results")
    st.sidebar.dataframe(st.session_state.results_df)
else:
    st.info("Upload a PDF file")

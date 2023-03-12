import streamlit as st
import base64
from pyresparser import ResumeParser


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def extract_data(file_path):
    data = ResumeParser(file_path).get_extracted_data()
    return data


st.title('Resume Analyser')

resume = st.file_uploader("Upload your resume",type=['pdf'])

if resume:
    with open('resume.pdf','wb') as f:
        f.write(resume.getbuffer())
        show_pdf("resume.pdf")

    st.write(extract_data("resume.pdf"))
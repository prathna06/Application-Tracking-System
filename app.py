import base64
import io
from dotenv import load_dotenv
from pdf2image import convert_from_path
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model= genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #convert pdf into img
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page =images[0]
        #byte conversion
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts =[
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
     raise FileNotFoundError("No file uploaded")

#Streamlit App
st.set_page_config(page_title="ATS Resume System")
st.header("Resume Analyser")
input_text = st.text_area("Job Description: ",key="input")
upload_file= st.file_uploader("Upload your resume(PDF)",type=["pdf"])

if upload_file is not None:
    st.write("PDF Uploaded Successfully")
submit1= st.button("Tell Me About the Resume")
#submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage Match with Resume")

input_prompt1= """ 
You are an experienced HR with tech experience in these fields software development, Full stack,
 web Developemnt,Product Management,Big Data,DEVOPS,Data Analyst your task is to review the provided
 resume against the job description for these profiles.
 Please share your professional evaluation on weather the candidate's profile aligns with
 Job description Highlight the strength and weeknesses of the candidates of the applicants in relation to the specific job role
"""
input_prompt2 = """
You are a Technical Human resource manager with expertise in software development, Full stack,
 web Developemnt,Product Management,Big Data,DEVOPS,Data Analyst
your role is to scrutinize the resume in light of the job description provided 
and it update the resume according to job description hihlight the changes
"""
input_prompt3=""" 
You are an skilled ATS (applicant Tracking System) scanner with a deep understanding of software development, Full stack,
 web Developemnt,Product Management,Big Data,DEVOPS,Data Analyst and deep ATS functionality, your task is
 to evaluate the resume against the provided job description. give me the percentage match with the job description
 First the output should come as percentage then keywords missing and last final thoughts.
"""
if submit1:
    if upload_file is not None:
      pdf_content = input_pdf_setup(upload_file)
      response = get_gemini_response(input_prompt1,pdf_content,input_text)
      st.subheader("The response is ")
      st.write(response)
    else:
      st.write("Please upload the resume")
#elif submit2:
 #   if upload_file is not None:
  #    pdf_content = input_pdf_setup(upload_file)
   #   response = get_gemini_response(input_prompt2,pdf_content,input_text)
    #  st.subheader("The response is ")
     # st.write(response)
    #else:
     # st.write("Please upload the resume")

elif submit3:
    if upload_file is not None:
      pdf_content = input_pdf_setup(upload_file)
      response = get_gemini_response(input_prompt3,pdf_content,input_text)
      st.subheader("The response is ")
      st.write(response)
    else:
      st.write("Please upload the resume")

      





import streamlit as st
from fpdf import FPDF
import base64

# Function to create a PDF bill
def create_pdf(data, language):
    pdf = FPDF()
    pdf.add_page()

    if language == "English":
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Bill Details", ln=True, align="C")
        pdf.ln(10)
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    else:
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt="تفصیلات بل", ln=True, align="C")
        pdf.ln(10)
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    return pdf.output(dest='S').encode('latin1')

def create_pdf(data, language):
    pdf = FPDF()
    pdf.add_page()

    if language == "English":
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Bill Details", ln=True, align="C")
        pdf.ln(10)
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    else:
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt="تفصیلات بل", ln=True, align="C")
        pdf.ln(10)
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf_file = pdf.output(dest='S').encode('latin1')
    b64 = base64.b64encode(pdf_file).decode()
    return f'data:application/pdf;base64,{b64}'

# Streamlit application
st.title("Bill Generation Application")

st.write("Please fill in the following details:")

name = st.text_input("Name / نام")
amount = st.text_input("Amount / رقم")
date = st.date_input("Date / تاریخ")
details = st.text_area("Details / تفصیل")

language = st.selectbox("Select Language / زبان منتخب کریں", ["English", "Urdu"])

if st.button("Generate Bill"):
    if not name or not amount or not date or not details:
        st.error("Please fill in all fields.")
    else:
        data = {
            "Name / نام": name,
            "Amount / رقم": amount,
            "Date / تاریخ": date,
            "Details / تفصیل": details
        }
        pdf = create_pdf(data, language)
        st.markdown(f'<a href="{pdf}" download="bill.pdf">Download Bill</a>', unsafe_allow_html=True)

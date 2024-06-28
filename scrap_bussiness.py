import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# Initialize session state
if "entries" not in st.session_state:
    st.session_state.entries = []

# Function to create a PDF bill
def create_pdf(entries, language):
    pdf = FPDF()
    pdf.add_page()

    if language == "English":
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Bill Details", ln=True, align="C")
        pdf.ln(10)
        for entry in entries:
            for key, value in entry.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
            pdf.ln(5)
    else:
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt="تفصیلات بل", ln=True, align="C")
        pdf.ln(10)
        for entry in entries:
            for key, value in entry.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
            pdf.ln(5)

    pdf_file = pdf.output(dest='S').encode('latin1')
    b64 = base64.b64encode(pdf_file).decode()
    return f'data:application/pdf;base64,{b64}'

# Streamlit application
st.title("Bill Generation Application")

st.write("Please fill in the following details:")

# Inputs for a new entry
name = st.text_input("Name / نام")
amount = st.text_input("Amount / رقم")
date = st.date_input("Date / تاریخ", datetime.now())
details = st.text_area("Details / تفصیل")

if st.button("Add Entry"):
    if not name or not amount or not date or not details:
        st.error("Please fill in all fields.")
    else:
        entry = {
            "Name / نام": name,
            "Amount / رقم": amount,
            "Date / تاریخ": date.strftime('%Y-%m-%d'),
            "Details / تفصیل": details
        }
        st.session_state.entries.append(entry)
        st.success("Entry added successfully!")

# Display current entries
if st.session_state.entries:
    st.write("Current Entries:")
    for i, entry in enumerate(st.session_state.entries):
        st.write(f"**Entry {i+1}:**")
        for key, value in entry.items():
            st.write(f"{key}: {value}")
        st.write("---")

# Language selection and PDF generation
language = st.selectbox("Select Language / زبان منتخب کریں", ["English", "Urdu"])

if st.button("Generate Bill"):
    if not st.session_state.entries:
        st.error("Please add at least one entry.")
    else:
        pdf = create_pdf(st.session_state.entries, language)
        st.markdown(f'<a href="{pdf}" download="bill.pdf">Download Bill</a>', unsafe_allow_html=True)

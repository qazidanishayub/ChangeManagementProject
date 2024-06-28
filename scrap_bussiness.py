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

    return pdf.output(dest='S')

# Streamlit application
st.title("Bill Generation Application")

st.write("Please fill in the following details:")

# Inputs for a new entry
name = st.text_input("Name / نام")
amount = st.text_input("Amount / رقم")
date = st.date_input("Date / تاریخ", datetime.now())
details = st.text_area("Details / تفصیل")
profit_share = st.text_input("Profit Share / منافع کا حصہ")
total_invested = st.text_input("Total Amount Invested / کل سرمایہ کاری کی رقم")
profit_duration = st.text_input("Profit Duration / منافع کی مدت")

if st.button("Add Entry"):
    if not name or not amount or not date or not details or not profit_share or not total_invested or not profit_duration:
        st.error("Please fill in all fields.")
    else:
        entry = {
            "Name / نام": name,
            "Amount / رقم": amount,
            "Date / تاریخ": date.strftime('%Y-%m-%d'),
            "Details / تفصیل": details,
            "Profit Share / منافع کا حصہ": profit_share,
            "Total Amount Invested / کل سرمایہ کاری کی رقم": total_invested,
            "Profit Duration / منافع کی مدت": profit_duration
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
        pdf_data = create_pdf(st.session_state.entries, language)
        pdf_data_b64 = base64.b64encode(pdf_data).decode()
        download_link = f'<a href="data:application/pdf;base64,{pdf_data_b64}" download="bill.pdf">Download Bill</a>'
        st.markdown(download_link, unsafe_allow_html=True)

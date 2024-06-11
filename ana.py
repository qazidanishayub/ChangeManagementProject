import streamlit as st
from streamlit_player import st_player
import random

# Define the tests and their types
tests = {
    "Listening": ["file_example_MP3_700KB.mp3"] ,
    "Visual": ["ForBiggerFun.mp4"] ,
}

# Function to evaluate Listening Test
def evaluate_listening(test_files):
    st.header("Listening Test")
    for idx, file in enumerate(test_files):
        st.subheader(f"Test {idx + 1}")
        st.audio(file)
        user_input = st.text_input(f"Evaluation for Test {idx + 1}", "")
        st.write(f"Your evaluation: {user_input}")

# Function to evaluate Visual Test
def evaluate_visual(test_files):
    st.header("Visual Test")
    for idx, file in enumerate(test_files):
        st.subheader(f"Test {idx + 1}")
        st.video(file)
        user_input = st.text_input(f"Evaluation for Test {idx + 1}", "")
        st.write(f"Your evaluation: {user_input}")

# Main function
def main():
    st.title("Accessible Neuropsychological Assessment (ANA)")
    
    # Signup Form
    st.sidebar.title("Signup Form")
    st.sidebar.subheader("Company/Educator Registration")
    is_company = st.sidebar.radio("You are:", ["company", "educator"])
    trade_name = st.sidebar.text_input("Trade name (if company):")
    corporate_name = st.sidebar.text_input("Corporate name (if company):")
    num_employees = st.sidebar.number_input("Number of employees (if company):")
    city_state = st.sidebar.text_input("City State:")
    cnpj_cpf = st.sidebar.text_input("CNPJ (company) or CPF (educator):")
    name_responsible = st.sidebar.text_input("Name - responsible:")
    profession_responsible = st.sidebar.text_input("Profession - responsible:")
    telephone = st.sidebar.text_input("Telephone:")
    email = st.sidebar.text_input("Email (login) - responsible:")
    password = st.sidebar.text_input("Login password:", type="password")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sign Up")
    st.sidebar.button("Register")

    st.sidebar.title("Select a Test")
    test_type = st.sidebar.radio("Choose the type of test:", ["Listening", "Visual", "Both"])

    if test_type == "Listening":
        evaluate_listening(tests["Listening"])
    elif test_type == "Visual":
        evaluate_visual(tests["Visual"])
    elif test_type == "Both":
        st.header("Combined Evaluation for Listening and Visual Tests")
        st.write("Please provide your evaluations for both the Listening and Visual tests side by side.")
        st.write("Listening Test:")
        evaluate_listening(tests["Listening"])
        st.write("Visual Test:")
        evaluate_visual(tests["Visual"])

if __name__ == "__main__":
    main()

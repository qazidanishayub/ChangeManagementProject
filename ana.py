import streamlit as st
from streamlit_player import st_player
import random

# Define the tests and their types
tests = {
    "Listening": ["file_example_MP3_700KB.mp3"],
    "Visual": ["ForBiggerFun.mp4"],
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
    st.sidebar.title("Select a Test")
    test_type = st.sidebar.radio("Choose the type of test:", ["Listening", "Visual", "Both"])

    if test_type == "Listening":
        evaluate_listening(tests["Listening"])
    elif test_type == "Visual":
        evaluate_visual(tests["Visual"])
    else:
        st.header("Listening and Visual Test")
        st.write("This section combines both listening and visual tests.")
        st.write("Instructions for the combined test will be provided soon.")

if __name__ == "__main__":
    main()

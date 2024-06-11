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

# Function to evaluate Both Tests
def evaluate_both(listening_files, visual_files):
    st.header("Both Tests")
    for idx, (listening_file, visual_file) in enumerate(zip(listening_files, visual_files)):
        st.subheader(f"Test {idx + 1}")
        st.audio(listening_file, format='audio/mp3', start_time=0)
        st.video(visual_file, start_time=0)
        st.write("Please provide your evaluation for both the Listening and Visual tests.")

# Main function
def main():
    st.title("Accessible Neuropsychological Assessment (ANA)")
    st.sidebar.title("Select a Test")
    test_type = st.sidebar.radio("Choose the type of test:", ["Listening", "Visual", "Both"])

    if test_type == "Listening":
        evaluate_listening(tests["Listening"])
    elif test_type == "Visual":
        evaluate_visual(tests["Visual"])
    elif test_type == "Both":
        evaluate_both(tests["Listening"], tests["Visual"])

if __name__ == "__main__":
    main()

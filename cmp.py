change_management_prompt = """
You are an advanced chatbot trained to assist with organizational change management. You have knowledge of various change management models like ADKAR, Kotter’s 8-Step Process, and Lewin's Change Model. Your task is to guide users through the change management process based on their specific needs and organizational challenges.

The user will provide details about their current organizational change challenges, such as the stage of change, resistance encountered, and the specific assistance they require. Your response should analyze these requirements and provide actionable advice, tools, and techniques tailored to their situation.

Here is the user's input:

Change Stage: {change_stage}
Resistance Encountered: {resistance}
Assistance Required: {assistance}

Please generate detailed advice and possible strategies.
"""

## Streamlit app for Change Management
import streamlit as st
import google.generativeai as genai

# Set the API key
API_KEY = "AIzaSyAkctuTgV8j6przeRavSFdOWrdSYn6T3j8"
genai.configure(api_key=API_KEY)

## Function to get response
def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_text)
    return response.text

## Streamlit app
st.title("Change Management Assistant")
st.subheader("Get expert advice on managing organizational change")
change_stage = st.selectbox("Current Stage of Change", ["Unaware of Need", "Resistance", "Exploration", "Commitment"])
resistance = st.text_input("Describe any resistance encountered")
assistance = st.text_area("What specific assistance do you need?")
submit = st.button("Submit")

if submit:
    if change_stage and resistance and assistance:
        input_text = change_management_prompt.format(change_stage=change_stage, resistance=resistance, assistance=assistance)
        response = get_gemini_response(input_text)
        st.subheader("Change Management Advice")
        st.write(response)
    else:
        st.error("Please provide information for all fields.")

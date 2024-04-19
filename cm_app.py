import streamlit as st
from openai import OpenAI

# Initialize API client with secure key management
OpenAI_key = st.secrets.openai_api_key
client = OpenAI(api_key=OpenAI_key)

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message

# Page configuration and theme setup for dark mode
st.set_page_config(page_title="Change Management Assessment Tool", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #202123;
        color: #fff;
    }
    .css-1yjuwjr {
        color: #fff;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title and Sidebar Setup
st.title("Change Management Assessment Tool")
selected_assessments = st.sidebar.multiselect("Select Assessments", assessments, default=None)

# Assessments and Questions Mapping (Sample from your document)
questions_dict = {
    "Change vision/case for change": [
        "What is the primary purpose of the change?",
        "How does this change align with the organization's goals?",
        "What specific outcomes do we aim to achieve with this change?"
    ],
    "Change approach/strategy": [
        "What are the key components of our change strategy?",
        "How will we communicate the change to stakeholders?",
        "What are the risks associated with this strategy?"
    ],
    "Change impact assessment": [
        "Who will be affected by this change?",
        "What are the potential risks?",
        "How will we mitigate these risks?"
    ],
    # Add other categories as per your document
}

# Handling chatbot conversation
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Assessment Interactions
for assessment in selected_assessments:
    st.header(f"{assessment} Assessment")
    questions = questions_dict.get(assessment, [])
    for question in questions:
        response_key = f"{assessment}: {question}"
        user_response = st.text_input(question, key=response_key)
        if st.button('Submit Response', key=response_key):
            bot_response = generate_response(user_response)
            st.session_state['conversation'].append({"question": question, "answer": bot_response})
            st.text_area("Bot Response", value=bot_response, height=100, key=f"response_{response_key}")

# Displaying the full conversation history if needed
if st.checkbox('Show full conversation history'):
    for exchange in st.session_state['conversation']:
        st.text_area("Question", exchange['question'], height=75)
        st.text_area("Answer", exchange['answer'], height=150)

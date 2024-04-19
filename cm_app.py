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

# Title and User Customization Setup
st.title("Change Management Assessment Tool")
st.sidebar.header("Customize Your Assessment")
details_level = st.sidebar.radio(
    "Select detail level",
    ("Basic", "Intermediate", "Advanced")
)

# Assessments Multi-Select
assessments = [
    "Change vision/case for change", "Change approach/strategy", "Change impact assessment",
    "Stakeholder assessment/map", "ADKAR assessment", "Training assessment", "Communications plan",
    "Engagement plan", "Training plan", "Key messages by stakeholder group", "Briefing messages",
    "Benefits/Adoption KPIs", "What’s changing and what is not summary", "Champions survey",
    "Users survey", "Training feedback survey", "Readiness assessment", "Health check",
    "Change KPIs/user adoption statistics", "Communications messages", "FAQs"
]
selected_assessments = st.sidebar.multiselect("Select Assessments", assessments, default=None)
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
    ]
    # Add other categories as per your document
}
# Assessment Dashboard Features
if st.sidebar.button("Create/Update Dashboard"):
    st.session_state['dashboard'] = selected_assessments
    st.success("Dashboard Updated!")

# Displaying Dashboard
if 'dashboard' in st.session_state:
    st.header("Your Custom Assessment Dashboard")
    for item in st.session_state['dashboard']:
        st.write(f"- {item}")

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
# Chatbot Interaction Based on Assessment
if st.button("Get Chatbot Response"):
    if not selected_assessments:
        prompt = "Please select at least one assessment to proceed."
        st.warning(prompt)
    else:
        prompt = f"Provide details for: {', '.join(selected_assessments)}"
        bot_response = generate_response(prompt)
        st.write("Chatbot Response:")
        st.write(bot_response)

# Signup Form Example (optional implementation as per initial setup)
with st.form("signup_form"):
    st.write("Sign up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Sign Up")

if submit_button:
    if username == "admin" and password == "123":
        st.success(f"Successfully signed up as {username}")
    else:
        st.error("Invalid username or password. Please try again.")


import streamlit as st
from openai import OpenAI

OpenAI_key = st.secrets.openai_api_key
client = OpenAI(api_key=OpenAI_key)

def generate_response(prompt):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[
       {"role": "system", "content": prompt},
    ]
    # temperature=0.2,
    # max_tokens=256,
    # top_p=1,
    )
    return response.choices[0].message
# Streamlit application
st.title("Change Management Assessment Tool")

# Sign-up form
with st.form("signup_form"):
    st.write("Sign up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Sign Up")

if submit_button:
    if username == "admin" and password == "123":
        st.success("Successfully signed up as {}".format(username))
    else:
        st.error("Invalid username or password. Please try again.")

# List of assessments
assessments = [
    "Change vision/case for change",
    "Change approach/strategy",
    "Change impact assessment",
    "Stakeholder assessment/map",
    "ADKAR assessment",
    "Training assessment",
    "Communications plan",
    "Engagement plan",
    "Training plan",
    "Key messages by stakeholder group",
    "Briefing messages",
    "Benefits/Adoption KPIs",
    "What’s changing and what is not summary",
    "Champions survey",
    "Users survey",
    "Training feedback survey",
    "Readiness assessment",
    "Health check",
    "Change KPIs/user adoption statistics",
    "Communications messages",
    "FAQs"
]

# Dropdown menu for assessment selection
selected_assessment = st.selectbox("Select Assessment", assessments, index=0)

# Chatbot response based on selected assessment
if st.button("Get Chatbot Response"):
    if selected_assessment == "All":
        prompt = "I would like to get information about all change management assessments."
    else:
        prompt = f"I would like to get information about {selected_assessment}."

    bot_response = generate_response(prompt)
    st.write("Chatbot Response:")
    st.write(bot_response)

import streamlit as st

# Step 1: Create a Streamlit application
st.title("Change Management Assessment Tool")

# Step 2: Design the user interface with sign-up and dropdown options
with st.form("signup_form"):
    st.write("Sign up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Sign Up")

if submit_button:
    st.success("Successfully signed up as {}".format(username))

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
    "Communications messages"
]

# Step 2 (continued): Display dropdown options
selected_assessment = st.selectbox("Select Assessment", assessments, index=0)


# Step 3: Add 'All' option and allow users to choose multiple assessments
if selected_assessment == "All":
    selected_assessments = assessments
else:
    selected_assessments = [selected_assessment]

# Step 4: Display selected assessments
st.write("Selected Assessments:")
for assessment in selected_assessments:
    st.write("- " + assessment)

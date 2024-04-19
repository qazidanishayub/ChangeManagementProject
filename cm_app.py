import streamlit as st
from openai import OpenAI

# Function to generate response from OpenAI API
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": " "}
        ]
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

# Initialize OpenAI client
OpenAI_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=OpenAI_key)

# Chat history
chat_history = []

# Main chat loop
while True:
    # User input
    user_input = st.text_input("You:", "")

    if st.button("Send"):
        # Add user input to chat history
        chat_history.append({"role": "user", "content": user_input})

        # Generate bot response
        bot_response = generate_response(user_input)

        # Add bot response to chat history
        chat_history.append({"role": "system", "content": bot_response})

        # Display chat history
        for message in chat_history:
            if message["role"] == "user":
                st.text_input("You:", value=message["content"], key=message["content"], disabled=True)
            else:
                st.text_input("Bot:", value=message["content"], key=message["content"], disabled=True)

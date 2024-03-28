import openai
import streamlit as st

# Streamlit page configuration
st.set_page_config(page_title="GPT Chatbot", page_icon=":robot_face:")

# Load your OpenAI API key from an environment variable or direct input
openai_api_key = st.secrets["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"] # Replace with your OpenAI API key

# Initialize the OpenAI client with your API key
openai.api_key = openai_api_key

# Define a function to get a response from OpenAI's completion engine
def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="davinci",  # You can use other engines as per your requirement
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.9
    )
    return response.choices[0].text.strip()

# Streamlit UI layout
st.title("GPT Chatbot")
st.write("Ask me anything!")

# Chat history is stored in a session state to persist across reruns
if 'history' not in st.session_state:
    st.session_state['history'] = []

# User input text box
user_input = st.text_input("Your message:", key="input")

# When the user sends a message, append it to the history and get a response
if st.button("Send") and user_input:
    # Append user input to history
    st.session_state['history'].append({"sender": "You", "message": user_input})
    # Get a response from GPT-3
    response = get_openai_response(user_input)
    # Append bot response to history
    st.session_state['history'].append({"sender": "Bot", "message": response})
    # Clear the text input
    st.session_state['input'] = ""

# Display chat history
for chat in st.session_state['history']:
    if chat['sender'] == "You":
        st.text_area("", value=chat['message'], height=50, key=str(chat)+'_you')
    else:
        st.text_area("", value=chat['message'], height=50, key=str(chat)+'_bot', disabled=True)

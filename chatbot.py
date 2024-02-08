# Import necessary libraries
import openai
import streamlit as st
import time
import os
import json
from dotenv import load_dotenv
load_dotenv()


# Set your OpenAI Assistant ID here
assistant_id = os.getenv("ASSISTANT_ID")

# Initialize the OpenAI client (ensure to set your API key in the sidebar within the app)
client = openai

# Initialize session state variables for file IDs and chat control
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Set up the Streamlit page with a title and icon
st.set_page_config(page_title="iUmrah", page_icon="🕋", layout="wide")
st.header("🕋 iUmrah Bot Assistant")

#Get the OPENAI API Key
openai_api_key_env = os.getenv('OPENAI_API_KEY')
#openai_api_key = st.sidebar.text_input(
#   'OpenAI API Key', placeholder='sk-', value=openai_api_key_env)
#url = "https://platform.openai.com/account/api-keys"
#st.sidebar.markdown("Get an Open AI Access Key [here](%s). " % url)
#if openai_api_key:
#    openai.api_key = openai_api_key

# Button to start the chat session
if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    # Create a thread once and store its ID in session state
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    #st.write("thread id: ", thread.id)

# Define the function to process messages with citations
def process_message_with_citations(message):
    message_content = message.content[0].text.value
    return message_content

# Only show the chat interface if the chat has been started
if st.session_state.start_chat:
   # st.write(getStockPrice('AAPL'))
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for the user
    if prompt := st.chat_input("How can I help you?"):
        # Add user message to the state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Create a run with additional instructions
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions = """
You are a bot that responds to user queries using the knowledge provided in the added files. 

When the user asks a question outside the scope of the files, please follow these guidelines:

- If it's a general Islamic question:
  - Respond with: "I am a bot that specializes in Umrah questions only. Please upgrade your account to answer general Islamic questions."

- If it's a non-Islamic and non-Umrah question:
  - Respond with: "I apologize, but I cannot answer your question. I am a bot that specializes in Umrah questions only."
"""
        )

        # Poll for the run to complete and retrieve the assistant's messages
        while run.status not in ["completed", "failed"]:
            st.sidebar.write(run.status)
            #if run.status == "requires_action":
            #    handle_function(run)
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        st.sidebar.write(run.status)

        # Retrieve messages added by the assistant
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            full_response = process_message_with_citations(message)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            with st.chat_message("assistant"):
                st.markdown(full_response, unsafe_allow_html=True)
import os
import json
from PIL import Image
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Streamlit page configuration
st.set_page_config(
    page_title="benGPT Chat",
    page_icon="🗼",
    layout="centered"
) 

# Retrieve API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is not set in the .env file.")
    st.stop()

# Set the API key as an environment variable
os.environ["GROQ_API_KEY"] = api_key

client = Groq()

# Initialize the chat history as Streamlit session state if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🗼 benGPT ChatBot")

st.markdown(
    """
    AI was created by God for the man's future. **>>>>>Unleash the power of AI with benGPT**

    I am your friend, so feel free to ask me any question.
    """
)

# Load and display image
image4 = Image.open("image4.png")
st.image(image4, use_column_width=True, width=300)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask benGPT...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are benGPT, a friendly and helpful AI assistant. When asked about your name, identify yourself as benGPT. Your creatorr is Benjamin Uka, a researcher and developer at Benjitable DS, a company that focuses on developing and applying various forms of artificial intelligence to help humans communicate more effectively"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Add a sidebar with a contact button and image
st.sidebar.title("About benGPT")
image2 = Image.open("image2.png")
st.sidebar.image(image2, caption="benGPT", use_column_width=True)

st.sidebar.markdown(
    """
    benGPT is a powerful AI assistant designed to learn and assist you with various tasks. 

    **Contact us:**
    * Email: benjaminukaimo@gmail.com
    * Phone: +2347067193071
    """
)

st.sidebar.button("Learn More")

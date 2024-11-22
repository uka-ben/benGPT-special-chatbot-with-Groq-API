import os
from PIL import Image
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="benGPT Chat",
    page_icon="🗼",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for background and styling
st.markdown(
    """
    <style>
        /* Background Image */
        .stApp {
            background-image: url('https://github.com/benGPT/benGPT-special-chatbot-with-Groq-API/blob/c51104cc26152d5a9219e3f8f485779acf190766/image3.png'); /* Replace this with the path to your image */
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: #ffffff; /* Ensure text is visible */
        }

        /* Slimmer Sidebar */
        [data-testid="stSidebar"] {
            width: 220px;
            background: linear-gradient(to bottom, #6c63ff, #ffffff);
            color: #ffffff;
            padding: 10px;
        }

        /* Sidebar Text Styling */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1 {
            color: #ffffff;
        }

        /* Main Page Title */
        .css-18ni7ap h1 {
            font-family: "Arial Black", sans-serif;
            font-size: 2.5rem;
            color: #ffffff;
            text-shadow: 2px 2px 5px #000000;
        }

        /* Chat Input Field */
        .stTextInput > div {
            background: #ffffff !important;
            border: 2px solid #6c63ff !important;
            border-radius: 10px;
        }

        /* Assistant Chat Styling */
        .stMarkdown {
            padding: 10px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.8);
        }

        /* Footer */
        footer {
            font-family: "Arial", sans-serif;
            text-align: center;
            color: #ffffff;
            padding: 20px;
            text-shadow: 1px 1px 3px #000000;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Retrieve API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize the chat history as Streamlit session state if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🗼 benGPT ChatBot")

# Welcome Message
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <p style="font-size: 20px; font-weight: bold;">
            AI was created by God for the man's future.<br>
            <span style="font-size: 22px;">**>>>>>Unleash the power of AI with benGPT**</span>
        </p>
        <p style="font-size: 16px;">I am your friend, so feel free to ask me any question.</p>
        <p style="font-size: 16px; color: #ffffff;"><b>Click the sidebar</b> >> for more on benGPT</p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
        {
            "role": "system",
            "content": (
                "You are benGPT, a friendly and helpful AI assistant. When asked about your name, identify yourself as benGPT. "
                "After each response, ask users to click the sidebar > for more. Always extend warm love and appreciation to users "
                "and be precise when possible. Your creator is Benjamin Uka, a researcher and developer at Benjitable DS, a company "
                "that focuses on developing and applying various forms of artificial intelligence to help humans communicate more effectively."
            ),
        },
        *st.session_state.chat_history,
    ]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Sidebar content
st.sidebar.title("About benGPT")
st.sidebar.markdown(
    """
    <div style="color: #ffffff;">
        <p><b>benGPT is a powerful AI assistant</b></p>
        <p>Designed to learn and assist you with various tasks.</p>
        <p style="font-size: 16px;"><b>Contact us:</b></p>
        <p>Email: <a href="mailto:benjaminukaimo@gmail.com" style="color: #ffffff;">benjaminukaimo@gmail.com</a></p>
        <p>Phone: +2347067193071</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.button("Learn More", help="Discover more about benGPT")

# Footer section
st.markdown(
    """
    <footer>
        © 2024 Benjitable DS - All Rights Reserved.
    </footer>
    """,
    unsafe_allow_html=True,
)

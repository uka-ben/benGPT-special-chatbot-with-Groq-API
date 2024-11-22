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

# Custom CSS for advanced styling
st.markdown(
    """
    <style>
        /* Slimmer Sidebar */
        [data-testid="stSidebar"] {
            width: 220px;
            background: linear-gradient(to bottom, #6c63ff, #ffffff);
            color: #ffffff;
            padding: 10px;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: #ffffff;
            font-family: "Arial", sans-serif;
        }
        [data-testid="stSidebar"] p {
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
        }

        /* Main Page Title */
        .css-18ni7ap h1 {
            font-family: "Arial Black", sans-serif;
            font-size: 2.5rem;
            color: #6c63ff;
        }

        /* Chat Input Field */
        .stTextInput > div {
            background: #ffffff !important;
            border: 2px solid #6c63ff !important;
            border-radius: 10px;
            font-family: "Arial", sans-serif;
        }

        /* Assistant Chat Styling */
        .stMarkdown {
            padding: 10px;
            border-radius: 8px;
        }
        .stMarkdown p {
            background: #e1f5fe;
            padding: 10px;
            border-radius: 8px;
        }

        /* Footer */
        footer {
            font-family: "Arial", sans-serif;
            text-align: center;
            color: #6c63ff;
            padding: 20px;
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
        <p style="font-size: 20px; font-weight: bold; color: #6c63ff;">
            AI was created by God for the man's future.<br>
            <span style="font-size: 22px;">**>>>>>Unleash the power of AI with benGPT**</span>
        </p>
        <p style="font-size: 16px; color: #444;">I am your friend, so feel free to ask me any question.</p>
        <p style="font-size: 16px; color: #6c63ff;"><b>Click the sidebar</b> >> for more on benGPT</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Load and display main image
image4 = Image.open("image4.png")
st.image(image4, use_column_width=True, caption="Welcome to benGPT", width=300)

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
image2 = Image.open("image2.png")
st.sidebar.image(image2, caption="benGPT", use_column_width=True)

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

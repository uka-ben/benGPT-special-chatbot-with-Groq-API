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

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Sidebar styles */
        [data-testid="stSidebar"] {
            width: 200px; /* Slimmer sidebar */
            background-color: #f0f0f5; /* Light background */
            border-right: 2px solid #6c63ff; /* Add a purple border */
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: #6c63ff;
        }
        [data-testid="stSidebar"] p {
            color: #333;
            font-weight: bold;
        }

        /* Page title */
        .css-18ni7ap h1 {
            color: #6c63ff !important; /* Purple title */
        }

        /* User input box */
        .stTextInput > div {
            background: #ffffff !important;
            border: 2px solid #6c63ff !important;
            border-radius: 8px;
        }

        /* Main chat messages styling */
        .stMarkdown {
            font-family: "Arial", sans-serif;
            font-size: 1.1rem;
            padding: 10px;
            border-radius: 10px;
        }

        /* Assistant chat messages */
        .stMarkdown p {
            background: #e1f5fe;
            padding: 10px;
            border-radius: 8px;
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

st.markdown(
    """
    <div style="text-align: center;">
        <p style="font-size: 18px; font-weight: bold; color: #6c63ff;">
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

# Add a styled sidebar
st.sidebar.title("About benGPT")
image2 = Image.open("image2.png")
st.sidebar.image(image2, caption="benGPT", use_column_width=True)

st.sidebar.markdown(
    """
    <div style="text-align: center; color: #444;">
        <p><b>benGPT is a powerful AI assistant</b></p>
        <p>Designed to learn and assist you with various tasks.</p>

        <p style="font-size: 16px; color: #6c63ff;"><b>Contact us:</b></p>
        <p>Email: benjaminukaimo@gmail.com</p>
        <p>Phone: +2347067193071</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.button("Learn More", help="Discover more about benGPT")

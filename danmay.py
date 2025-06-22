import os
import json
from PIL import Image
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay Academy School Chat",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="expanded"
) 

# Custom CSS to control the sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 250px;  /* Adjust this value for desired width */
        min-width: 250px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Groq client with API key
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Initialize the chat history as Streamlit session state if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🏫 Danmay Academy School Assistant")

st.markdown(
    """
    Welcome to Danmay Academy's learning assistant! **>>>>>Your educational companion for nursery, primary, and secondary school learning<<<<<**

    I'm here to help students with their studies, answer questions, and provide educational support.
    Click the side bar >> for more information about our school.
    """
)

# Load and display image
image4 = Image.open("image4.png")
st.image(image4, width=300, use_container_width=True)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask your school assistant...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are Danmay Academy's educational assistant, a friendly and helpful AI for students. Your purpose is to assist nursery, primary, and secondary school students with their learning. Be patient, encouraging, and adapt your explanations to the student's level. When asked about your name, identify yourself as Danmay Assistant. After each response, invite users to click the sidebar for more school information. Always maintain a professional yet warm tone suitable for educational settings."},
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

# Add a sidebar with school information
st.sidebar.title("About Danmay Academy")
image2 = Image.open("image2.png")
st.sidebar.image(image2, caption="Danmay Academy", use_container_width=True)

st.sidebar.markdown(
    """
    **Danmay Academy** is a premier educational institution offering:
    - Nursery School
    - Primary Education
    - Secondary School
    
    Our mission is to provide quality education in a nurturing environment.
    
    **School Hours:**
    Monday-Friday: 8:00 AM - 3:00 PM
    
    **Contact us:**
    - Email: info@danmayacademy.edu
    - Phone: +234123456789
    - Address: 123 Education Street, Learning City
    """
)

st.sidebar.button("School Calendar")

st.sidebar.title("Our Facilities")
image5 = Image.open("image5.png")
st.sidebar.image(image5, caption="School Library", use_container_width=True)
import os
import json
from PIL import Image
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay International Academy",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
) 

# Custom CSS for enhanced styling
st.markdown("""
<style>
    :root {
        --primary: #2E86AB;
        --secondary: #F18F01;
        --accent: #A23B72;
        --light: #F7F7FF;
        --dark: #2B2D42;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: var(--light);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--primary) !important;
        color: white;
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
    }
    
    [data-testid="stChatMessageContent"] {
        font-size: 1.1rem;
    }
    
    .user-message {
        background-color: var(--secondary) !important;
        color: white;
    }
    
    .assistant-message {
        background-color: var(--primary) !important;
        color: white;
    }
    
    .stButton>button {
        background-color: var(--accent) !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    .stSelectbox, .stTextInput {
        border-radius: 8px;
    }
    
    .header {
        color: var(--primary);
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .welcome-card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .info-card {
        background-color: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .sidebar-title {
        color: white !important;
        font-size: 1.5rem !important;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# School logo and header
def render_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="header">
            <h1 style="color: white; margin: 0;">🏫 Danmay International Academy</h1>
            <p style="color: white; margin: 0;">Excellence in Education</p>
        </div>
        """, unsafe_allow_html=True)

# User information form
if not st.session_state.user_info:
    render_header()
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("user_info_form"):
                st.markdown("""
                <div class="welcome-card">
                    <h3 style="color: var(--primary); text-align: center;">Welcome to Our Learning Assistant</h3>
                    <p style="text-align: center;">Please provide your information to continue</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.container():
                    age_range = st.selectbox(
                        "📏 Age Range",
                        ["3-5 (Creche/Nursery)", "6-10 (Primary)", "11-16 (Secondary)"],
                        index=None,
                        placeholder="Select your age range..."
                    )
                    
                    gender = st.selectbox(
                        "👦👧 Gender",
                        ["Male", "Female", "Prefer not to say"],
                        index=None,
                        placeholder="Select your gender..."
                    )
                    
                    class_level = st.selectbox(
                        "📚 Class Level",
                        ["Creche", "Nursery 1", "Nursery 2", "Primary 1", "Primary 2", 
                         "Primary 3", "Primary 4", "Primary 5", "Primary 6", "JSS 1", 
                         "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"],
                        index=None,
                        placeholder="Select your class..."
                    )
                    
                    submitted = st.form_submit_button("👉 Begin Learning", use_container_width=True)
                    
                    if submitted:
                        if age_range and gender and class_level:
                            st.session_state.user_info = {
                                "age_range": age_range,
                                "gender": gender,
                                "class_level": class_level
                            }
                            st.rerun()
                        else:
                            st.warning("Please fill in all fields")

    # School information in sidebar
    with st.sidebar:
        st.markdown('<p class="sidebar-title">About Our School</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            <p><strong>🏆 Premier Education:</strong><br>
            Creche to Secondary level</p>
            <p><strong>🌟 Mission:</strong><br>
            Safe, stimulating learning environment</p>
            <p><strong>✨ Vision:</strong><br>
            Excellence in morals, academics, discipline</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# Main chat interface
render_header()

# Student info card
st.markdown(f"""
<div class="welcome-card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="color: var(--primary); margin: 0;">Welcome, {st.session_state.user_info['gender']} student!</h3>
            <p style="margin: 0;">Class: {st.session_state.user_info['class_level']} | Age: {st.session_state.user_info['age_range']}</p>
        </div>
        <div style="background-color: var(--primary); color: white; padding: 8px 16px; border-radius: 20px;">
            🎓 Learning Mode
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="stChatMessage user-message">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-weight: bold;">You:</div>
                <div>{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stChatMessage assistant-message">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-weight: bold;">Assistant:</div>
                <div>{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_prompt = st.chat_input("💬 Ask your educational question...")

if user_prompt:
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # Prepare messages for LLM
    messages = [
        {
            "role": "system", 
            "content": f"""You are Danmay International Academy's educational assistant for a {st.session_state.user_info['age_range']} student in {st.session_state.user_info['class_level']}.
            
            STRICT RULES:
            1. ONLY respond to educational questions related to school subjects, homework, or school activities
            2. For non-educational questions, respond: "I'm sorry, I can only assist with educational matters. Please ask about your school work or subjects."
            3. Maintain a professional, encouraging tone suitable for {st.session_state.user_info['age_range']} students
            4. Adapt explanations to {st.session_state.user_info['class_level']} level
            5. Never provide personal opinions or non-educational advice
            
            Current Subjects (adjust based on class level):
            - Nursery: Literacy, Numeracy, Social Habits
            - Primary: English, Math, Science, Social Studies
            - Secondary: English, Math, Sciences, Humanities
            
            School Values: Excellence, Discipline, Moral Values"""
        },
        *st.session_state.chat_history
    ]

    # Get LLM response
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    st.rerun()

# Sidebar information
with st.sidebar:
    st.markdown('<p class="sidebar-title">Student Profile</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <p><strong>👤 Student:</strong> {st.session_state.user_info['gender']}</p>
        <p><strong>📏 Age Range:</strong> {st.session_state.user_info['age_range']}</p>
        <p><strong>🏫 Class:</strong> {st.session_state.user_info['class_level']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">Quick Links</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <p><a href="#" style="color: var(--accent);">📚 School Portal</a></p>
        <p><a href="#" style="color: var(--accent);">🗓️ Academic Calendar</a></p>
        <p><a href="#" style="color: var(--accent);">📝 Homework Help</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">School Contacts</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <p>📧 danmayinternational.com.ng</p>
        <p>📞 08038965253</p>
        <p>📞 09051906862</p>
        <p>🏠 Opposite UDSS, Camp David Street, Aluu</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Change Student Information", use_container_width=True):
        st.session_state.user_info = None
        st.rerun()
import streamlit as st
from groq import Groq
from PIL import Image
import os

# Streamlit page configuration - hide all Streamlit branding
st.set_page_config(
    page_title="Danmay International Academy",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide ALL Streamlit branding and style elements
st.markdown("""
<style>
    /* Hide ALL Streamlit branding elements */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .st-emotion-cache-1wbqy5l {display: none;}
    .st-emotion-cache-h5rgaw {visibility: hidden;}
    
    /* Hide the 'Made with Streamlit' footer */
    .reportview-container .main footer {visibility: hidden;}
    .reportview-container .main footer:after {
        content: "";
        visibility: hidden;
    }
    
    /* Hide hamburger menu */
    #MainMenu {visibility: hidden;}
    
    /* Hide decorative elements */
    .stDecoration {display: none;}
    
    /* Hide the Streamlit toolbar */
    .stToolbar {display: none;}
    
    /* Main content styling */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        padding: 2rem;
    }
    
    /* Card styling */
    .info-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #2E86AB;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
    }
    
    .user-message {
        background-color: #F18F01 !important;
        color: white !important;
    }
    
    .assistant-message {
        background-color: #2E86AB !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #A23B72 !important;
        color: white !important;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
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

# Load logo from root directory
def load_logo():
    try:
        logo = Image.open("danmaylogo.png")
        return logo
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None

# School logo and header
def render_header():
    logo = load_logo()
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    
    if logo:
        st.image(logo, width=180)
    else:
        st.markdown("🏫", unsafe_allow_html=True)
    
    st.markdown("""
        <h1 style="color: #2E86AB;">Danmay International Academy</h1>
        <p style="color: #555555;">Excellence in Education from Creche to Secondary</p>
        </div>
    """, unsafe_allow_html=True)

# User information form
if not st.session_state.user_info:
    render_header()
    
    with st.container():
        with st.form("user_info_form"):
            st.markdown("""
            <div class="info-card">
                <h3 style="color: #2E86AB; text-align: center;">🎓 Welcome to Our Learning Assistant</h3>
                <p style="text-align: center;">Please provide your information to continue</p>
            </div>
            """, unsafe_allow_html=True)
            
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
            
            submitted = st.form_submit_button("🚀 Begin Learning", use_container_width=True)
            
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

    # School information section (only shown before chat starts)
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #2E86AB; border-bottom: 2px solid #F18F01; padding-bottom: 0.5rem;">About Our School</h3>
        <p><strong>🏆 Premier Education:</strong><br>
        From Creche to Secondary level</p>
        <p><strong>🌟 Mission:</strong><br>
        Safe, stimulating learning environment</p>
        <p><strong>✨ Vision:</strong><br>
        Excellence in morals, academics, discipline</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact information section (only shown before chat starts)
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #2E86AB; border-bottom: 2px solid #F18F01; padding-bottom: 0.5rem;">Contact Information</h3>
        <p>📧 danmayinternational.com.ng</p>
        <p>📞 08038965253</p>
        <p>📞 09051906862</p>
        <p>🏠 Opposite UDSS, Camp David Street, Aluu</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Main chat interface (only shown after user info is submitted)
render_header()

# Student info card
st.markdown(f"""
<div class="info-card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="color: #2E86AB; margin: 0;">👋 Welcome, {st.session_state.user_info['gender']} student!</h3>
            <p style="margin: 0;">📚 Class: {st.session_state.user_info['class_level']} | 📏 Age: {st.session_state.user_info['age_range']}</p>
        </div>
        <div style="background-color: #A23B72; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem;">
            🎓 Learning Mode
        </div>
    </div>
    <div style="margin-top: 1rem;">
        <p style="margin: 0.5rem 0; font-weight: bold;">📖 Suggested Subjects:</p>
        <div>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">English</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Mathematics</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Science</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Social Studies</span>
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
                <div style="font-weight: bold; font-size: 1.2rem;">👤 You:</div>
                <div>{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stChatMessage assistant-message">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-weight: bold; font-size: 1.2rem;">🏫 Assistant:</div>
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

# Change student information button (shown below chat)
if st.button("🔄 Change Student Information", use_container_width=True):
    st.session_state.user_info = None
    st.session_state.chat_history = []
    st.rerun()
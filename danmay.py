import streamlit as st
from groq import Groq
from PIL import Image
import os

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay International Academy",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Custom CSS with improved readability
st.markdown("""
<style>
    /* Show sidebar expander */
    [data-testid="collapsedControl"] {
        display: block !important;
        color: black !important;
    }
    
    /* Main text color */
    body, .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        color: black !important;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: black !important;
    }
    
    /* Card text color */
    .info-card, .welcome-card {
        color: black !important;
    }
    
    /* Chat message text */
    .stChatMessage {
        color: black !important;
    }
    
    /* Button text */
    .stButton>button {
        color: white !important;
    }
    
    /* Original styling with improved contrast */
    :root {
        --primary: #2E86AB;
        --secondary: #F18F01;
        --accent: #A23B72;
        --light: #FFFFFF;  /* Changed to pure white */
        --dark: #000000;   /* Pure black for text */
        --card-bg: #FFFFFF;
        --sidebar-bg: #FFFFFF; /* White background */
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: var(--light);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid #E0E0E0;
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: var(--secondary) !important;
        color: white !important;
        border-left: 5px solid #D97B00;
    }
    
    .assistant-message {
        background-color: var(--primary) !important;
        color: white !important;
        border-left: 5px solid #1C5D7F;
    }
    
    .stButton>button {
        background-color: var(--accent) !important;
        color: white !important;
    }
    
    .header-container {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white !important;
    }
    
    .sidebar-title {
        color: var(--dark) !important;
    }
    
    .info-card, .welcome-card {
        color: var(--dark) !important;
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
    logo = load_logo()
    st.markdown("""
    <div class="header-container" style="padding: 1.5rem; border-radius: 0 0 15px 15px; margin-bottom: 2rem; text-align: center;">
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
    """, unsafe_allow_html=True)
    
    if logo:
        st.image(logo, width=180)
    else:
        st.markdown("🏫", unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        <h1 style="margin: 0; color: white !important;">Danmay International Academy</h1>
        <p style="margin: 0; color: white !important; opacity: 0.9;">Excellence in Education from Creche to Secondary</p>
    </div>
    """, unsafe_allow_html=True)

# [Rest of your application code remains exactly the same]
# [Only the CSS and color handling has been modified]

# User information form
if not st.session_state.user_info:
    render_header()
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("user_info_form"):
                st.markdown("""
                <div style="background-color: white; border-radius: 15px; padding: 1.5rem; margin-bottom: 1.5rem;">
                    <h3 style="color: #2E86AB; text-align: center;">🎓 Welcome to Our Learning Assistant</h3>
                    <p style="text-align: center; color: black;">Please provide your information to continue</p>
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

    # School information in sidebar
    with st.sidebar:
        st.markdown('<p style="color: black !important; font-size: 1.3rem; text-align: center; border-bottom: 2px solid #F18F01; padding-bottom: 0.5rem;">About Our School</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: white; border-radius: 15px; padding: 1rem; margin-bottom: 1rem; color: black !important;">
            <p><strong>🏆 Premier Education:</strong><br>
            From Creche to Secondary level</p>
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
<div style="background-color: white; border-radius: 15px; padding: 1.5rem; margin-bottom: 1.5rem; color: black !important;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="color: #2E86AB; margin: 0;">👋 Welcome, {st.session_state.user_info['gender']} student!</h3>
            <p style="margin: 0; color: black !important;">📚 Class: {st.session_state.user_info['class_level']} | 📏 Age: {st.session_state.user_info['age_range']}</p>
        </div>
        <div style="background-color: #A23B72; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem;">
            🎓 Learning Mode
        </div>
    </div>
    <div style="margin-top: 1rem;">
        <p style="margin: 0.5rem 0; font-weight: bold; color: black !important;">📖 Suggested Subjects:</p>
        <div>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">English</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Mathematics</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Science</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Social Studies</span>
            <span style="background-color: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; margin-right: 5px; display: inline-block;">Moral Instruction</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message" style="border-radius: 15px; padding: 12px; margin: 8px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-weight: bold; font-size: 1.2rem; color: white !important;">👤 You:</div>
                <div style="color: white !important;">{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message" style="border-radius: 15px; padding: 12px; margin: 8px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-weight: bold; font-size: 1.2rem; color: white !important;">🏫 Assistant:</div>
                <div style="color: white !important;">{message["content"]}</div>
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
    st.markdown('<p style="color: black !important; font-size: 1.3rem; text-align: center; border-bottom: 2px solid #F18F01; padding-bottom: 0.5rem;">Student Profile</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color: white; border-radius: 15px; padding: 1rem; margin-bottom: 1rem; color: black !important;">
        <p><strong>👤 Student:</strong> {st.session_state.user_info['gender']}</p>
        <p><strong>📏 Age Range:</strong> {st.session_state.user_info['age_range']}</p>
        <p><strong>🏫 Class:</strong> {st.session_state.user_info['class_level']}</p>
        <p><strong>📅 Last Active:</strong> Now</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: black !important; font-size: 1.3rem; text-align: center; border-bottom: 2px solid #F18F01; padding-bottom: 0.5rem;">Quick Links</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: white; border-radius: 15px; padding: 1rem; margin-bottom: 1rem; color: black !important;">
        <p><a href="#" style="color: #A23B72 !important; text-decoration: none;">📚 School Portal</a></p>
        <p><a href="#" style="color: #A23B72 !important; text-decoration: none;">🗓️ Academic Calendar</a></p>
        <p><a href="#" style="color: #A23B72 !important; text-decoration: none;">📝 Homework Help</a></p>
        <p><a href="#" style="color: #A23B72 !important; text-decoration: none;">🏆 Student Resources</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: black !important; font-size: 1.3rem; text-align: center; border-bottom: 2px solid #F18F01; padding-bottom: 0.5rem;">School Contacts</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: white; border-radius: 15px; padding: 1rem; margin-bottom: 1rem; color: black !important;">
        <p>📧 danmayinternational.com.ng</p>
        <p>📞 08038965253</p>
        <p>📞 09051906862</p>
        <p>🏠 Opposite UDSS, Camp David Street, Aluu</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Change Student Information", use_container_width=True):
        st.session_state.user_info = None
        st.rerun()
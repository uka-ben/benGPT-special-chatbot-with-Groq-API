import streamlit as st
from groq import Groq
from PIL import Image
import requests
from io import BytesIO

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay International Academy",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load logo from repository
def load_logo():
    try:
        logo_url = "https://raw.githubusercontent.com/uka-ben/benGPT-special-chatbot-with-Groq-API/blob/master/danmaylogo.png"
        response = requests.get(logo_url)
        logo = Image.open(BytesIO(response.content))
        return logo
    except:
        return None

# Custom CSS with all requested changes
st.markdown("""
<style>
    /* Hide all Streamlit default elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Color variables */
    :root {
        --primary: #2E86AB;
        --secondary: #F18F01;
        --accent: #A23B72;
        --light: #F7F7FF;
        --dark: #2B2D42;
        --card-bg: #FFFFFF;
        --sidebar-bg: #F0F2F6;
        --text-dark: #333333;
    }
    
    /* Main app styling */
    [data-testid="stAppViewContainer"] {
        background-color: var(--light);
    }
    
    /* Sidebar styling - now with dark text */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid #E0E0E0;
        color: var(--text-dark) !important;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: var(--secondary) !important;
        color: white;
        border-left: 5px solid #D97B00;
    }
    
    .assistant-message {
        background-color: var(--primary) !important;
        color: white;
        border-left: 5px solid #1C5D7F;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--accent) !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Card styling */
    .welcome-card {
        background-color: var(--card-bg);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid var(--accent);
    }
    
    .info-card {
        background-color: var(--card-bg);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 3px solid var(--secondary);
        color: var(--text-dark);
    }
    
    /* Sidebar title - now with dark text */
    .sidebar-title {
        color: var(--text-dark) !important;
        font-size: 1.3rem !important;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        border-bottom: 2px solid var(--secondary);
        padding-bottom: 0.5rem;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .logo-img {
        max-width: 180px;
        height: auto;
    }
    
    /* Badge styling */
    .badge {
        background-color: var(--accent);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Subject tags */
    .subject-tag {
        background-color: var(--primary);
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-right: 5px;
        margin-bottom: 5px;
        display: inline-block;
    }
    
    /* Links styling */
    .sidebar-link {
        color: var(--accent) !important;
        text-decoration: none !important;
        transition: color 0.3s;
    }
    
    .sidebar-link:hover {
        color: var(--primary) !important;
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
    <div class="header-container">
        <div class="logo-container">
    """, unsafe_allow_html=True)
    
    if logo:
        st.image(logo, width=180)
    else:
        st.markdown("🏫", unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        <h1 style="margin: 0; color: white;">Danmay International Academy</h1>
        <p style="margin: 0; color: white; opacity: 0.9;">Excellence in Education from Creche to Secondary</p>
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
                    <h3 style="color: var(--primary); text-align: center;">🎓 Welcome to Our Learning Assistant</h3>
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
        st.markdown('<p class="sidebar-title">About Our School</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
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
<div class="welcome-card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="color: var(--primary); margin: 0;">👋 Welcome, {st.session_state.user_info['gender']} student!</h3>
            <p style="margin: 0;">📚 Class: {st.session_state.user_info['class_level']} | 📏 Age: {st.session_state.user_info['age_range']}</p>
        </div>
        <div class="badge">
            🎓 Learning Mode
        </div>
    </div>
    <div style="margin-top: 1rem;">
        <p style="margin: 0.5rem 0; font-weight: bold;">📖 Suggested Subjects:</p>
        <div>
            <span class="subject-tag">English</span>
            <span class="subject-tag">Mathematics</span>
            <span class="subject-tag">Science</span>
            <span class="subject-tag">Social Studies</span>
            <span class="subject-tag">Moral Instruction</span>
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

# Sidebar information
with st.sidebar:
    st.markdown('<p class="sidebar-title">Student Profile</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <p><strong>👤 Student:</strong> {st.session_state.user_info['gender']}</p>
        <p><strong>📏 Age Range:</strong> {st.session_state.user_info['age_range']}</p>
        <p><strong>🏫 Class:</strong> {st.session_state.user_info['class_level']}</p>
        <p><strong>📅 Last Active:</strong> Now</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">Quick Links</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <p><a href="#" class="sidebar-link">📚 School Portal</a></p>
        <p><a href="#" class="sidebar-link">🗓️ Academic Calendar</a></p>
        <p><a href="#" class="sidebar-link">📝 Homework Help</a></p>
        <p><a href="#" class="sidebar-link">🏆 Student Resources</a></p>
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
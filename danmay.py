import os
import json
from PIL import Image
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay International Academy Chat",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="expanded"
) 

# Custom CSS
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 250px;
        min-width: 250px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Groq client
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# User information form
if not st.session_state.user_info:
    st.title("🏫 Danmay International Academy")
    st.subheader("Please provide your information to continue")
    
    with st.form("user_info_form"):
        age_range = st.selectbox(
            "Age Range",
            ["3-5 (Creche/Nursery)", "6-10 (Primary)", "11-16 (Secondary)"],
            index=None,
            placeholder="Select your age range..."
        )
        
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Prefer not to say"],
            index=None,
            placeholder="Select your gender..."
        )
        
        class_level = st.selectbox(
            "Class Level",
            ["Creche", "Nursery 1", "Nursery 2", "Primary 1", "Primary 2", 
             "Primary 3", "Primary 4", "Primary 5", "Primary 6", "JSS 1", 
             "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"],
            index=None,
            placeholder="Select your class..."
        )
        
        submitted = st.form_submit_button("Submit")
        
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
    st.sidebar.title("About Our School")
    st.sidebar.markdown("""
    **Danmay International Academy**  
    Offering quality education from Creche to Secondary level.
    
    **Mission:** Providing safe, stimulating learning environment.
    **Vision:** Excellence in morals, academics, and discipline.
    """)
    st.stop()

# Main chat interface
st.title(f"🏫 Danmay Academy Assistant - {st.session_state.user_info['class_level']}")
st.markdown(f"""
Welcome, {st.session_state.user_info['gender']} student from {st.session_state.user_info['class_level']}!

**This assistant is for educational purposes only.**  
Please ask questions related to your studies.
""")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Ask your educational question...")

if user_prompt:
    # Add user message to chat
    st.chat_message("user").markdown(user_prompt)
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

    # Display response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Sidebar information
st.sidebar.title("Student Information")
st.sidebar.write(f"""
**Age Range:** {st.session_state.user_info['age_range']}  
**Gender:** {st.session_state.user_info['gender']}  
**Class:** {st.session_state.user_info['class_level']}
""")

st.sidebar.markdown("---")
st.sidebar.title("School Contacts")
st.sidebar.markdown("""
- Email: danmayinternational.com.ng  
- Phone: 08038965253, 09051906862  
- Address: Opposite UDSS, Camp David Street, Aluu, Port Harcourt
""")

# Reset button
if st.sidebar.button("Change Student Information"):
    st.session_state.user_info = None
    st.rerun()
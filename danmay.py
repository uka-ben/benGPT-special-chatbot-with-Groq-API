import streamlit as st
from groq import Groq
from PIL import Image
import sqlite3
import os
import hashlib
import datetime
from io import BytesIO
import time

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay International Academy",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS styling with vibrant colors
st.markdown("""
<style>
    /* Hide header and footer */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main content styling */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
    }
    
    /* Card styling */
    .info-card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #6a11cb;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%) !important;
        color: white !important;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 1rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Section title styling */
    .section-title {
        color: #6a11cb;
        border-bottom: 3px solid #ff758c;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        font-weight: bold;
    }
    
    /* Profile picture styling */
    .profile-pic {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto;
        display: block;
        border: 3px solid #6a11cb;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Table styling */
    .timetable {
        width: 100%;
        border-collapse: collapse;
    }
    
    .timetable th, .timetable td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
    }
    
    .timetable th {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
    }
    
    .timetable tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    /* Homework card styling */
    .homework-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #ff758c;
    }
    
    .homework-title {
        font-weight: bold;
        color: #6a11cb;
        font-size: 1.1rem;
    }
    
    .homework-due {
        font-size: 0.8rem;
        color: #666;
    }
    
    .homework-status {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .submitted {
        background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
        color: white;
    }
    
    .pending {
        background: linear-gradient(135deg, #FFC107 0%, #FFD54F 100%);
        color: black;
    }
    
    /* Admin specific styles */
    .admin-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #2575fc;
    }
    
    /* Landing page styles */
    .landing-feature {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .landing-feature:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #6a11cb;
    }
    
    /* Disappearing message */
    .disappearing-message {
        animation: fadeOut 5s forwards;
    }
    
    @keyframes fadeOut {
        0% { opacity: 1; }
        100% { opacity: 0; height: 0; padding: 0; margin: 0; }
    }
    
    /* Message bubbles */
    .message-bubble {
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        word-wrap: break-word;
    }
    
    .student-message {
        background: #e3f2fd;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .admin-message {
        background: #bbdefb;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Parent info card */
    .parent-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
api_key = st.secrets.get("GROQ_API_KEY")
if api_key:
    client = Groq(api_key=api_key)
else:
    st.error("GROQ_API_KEY not found in secrets")
    st.stop()

# Database setup
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  role TEXT CHECK(role IN ('admin', 'student')),
                  full_name TEXT,
                  class_level TEXT,
                  profile_pic BLOB,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create homework table
    c.execute('''CREATE TABLE IF NOT EXISTS homework
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  subject TEXT,
                  title TEXT,
                  description TEXT,
                  file_data BLOB,
                  file_name TEXT,
                  file_type TEXT,
                  submitted_at TIMESTAMP,
                  status TEXT DEFAULT 'pending',
                  feedback TEXT,
                  FOREIGN KEY(student_id) REFERENCES users(id))''')
    
    # Create timetable table
    c.execute('''CREATE TABLE IF NOT EXISTS timetable
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class_level TEXT,
                  day TEXT,
                  period INTEGER,
                  subject TEXT,
                  teacher TEXT,
                  room TEXT)''')
    
    # Create messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sender_id INTEGER,
                  receiver_id INTEGER,
                  message TEXT,
                  is_admin_broadcast BOOLEAN DEFAULT 0,
                  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  is_read BOOLEAN DEFAULT 0,
                  FOREIGN KEY(sender_id) REFERENCES users(id),
                  FOREIGN KEY(receiver_id) REFERENCES users(id))''')
    
    # Create parents table
    c.execute('''CREATE TABLE IF NOT EXISTS parents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER UNIQUE,
                  parent_name TEXT,
                  address TEXT,
                  phone TEXT,
                  email TEXT,
                  nationality TEXT,
                  children_in_school INTEGER,
                  debts_owed REAL,
                  remarks TEXT,
                  FOREIGN KEY(student_id) REFERENCES users(id))''')
    
    # Insert sample timetable if empty
    c.execute("SELECT COUNT(*) FROM timetable")
    if c.fetchone()[0] == 0:
        sample_timetable = [
            ('SSS 1', 'Monday', 1, 'Mathematics', 'Mr. Johnson', 'Room 101'),
            ('SSS 1', 'Monday', 2, 'English', 'Mrs. Smith', 'Room 102'),
            ('SSS 1', 'Monday', 3, 'Physics', 'Mr. Brown', 'Lab 1'),
            ('SSS 1', 'Tuesday', 1, 'Chemistry', 'Mrs. Davis', 'Lab 2'),
            ('SSS 1', 'Tuesday', 2, 'Biology', 'Mr. Wilson', 'Lab 1'),
            ('SSS 1', 'Wednesday', 1, 'Mathematics', 'Mr. Johnson', 'Room 101'),
            ('SSS 1', 'Wednesday', 2, 'Geography', 'Mrs. Taylor', 'Room 103'),
            ('SSS 1', 'Thursday', 1, 'English', 'Mrs. Smith', 'Room 102'),
            ('SSS 1', 'Thursday', 2, 'Economics', 'Mr. Clark', 'Room 104'),
            ('SSS 1', 'Friday', 1, 'Computer Science', 'Mr. Adams', 'Computer Lab'),
        ]
        c.executemany("INSERT INTO timetable (class_level, day, period, subject, teacher, room) VALUES (?, ?, ?, ?, ?, ?)", sample_timetable)
    
    # Insert admin user if not exists
    c.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if c.fetchone()[0] == 0:
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                  ("admin", admin_password, "admin", "Administrator"))
    
    conn.commit()
    conn.close()

init_db()

# Database helper functions
def get_db_connection():
    return sqlite3.connect('school.db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("SELECT id, username, role, full_name, class_level, profile_pic FROM users WHERE username=? AND password=?", 
              (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password, role, full_name, class_level=None, profile_pic=None):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password, role, full_name, class_level, profile_pic) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, hashed_password, role, full_name, class_level, profile_pic))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_student_profile(student_id, full_name, class_level, profile_pic=None):
    conn = get_db_connection()
    c = conn.cursor()
    if profile_pic:
        c.execute("UPDATE users SET full_name=?, class_level=?, profile_pic=? WHERE id=?", 
                  (full_name, class_level, profile_pic, student_id))
    else:
        c.execute("UPDATE users SET full_name=?, class_level=? WHERE id=?", 
                  (full_name, class_level, student_id))
    conn.commit()
    conn.close()

def get_students():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, full_name, class_level FROM users WHERE role='student'")
    students = c.fetchall()
    conn.close()
    return students

def get_timetable(class_level):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT day, period, subject, teacher, room FROM timetable WHERE class_level=? ORDER BY day, period", (class_level,))
    timetable = c.fetchall()
    conn.close()
    return timetable

def submit_homework(student_id, subject, title, description, file_data, file_name, file_type):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO homework (student_id, subject, title, description, file_data, file_name, file_type, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (student_id, subject, title, description, file_data, file_name, file_type, datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_student_homework(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, subject, title, description, file_name, submitted_at, status, feedback FROM homework WHERE student_id=? ORDER BY submitted_at DESC", (student_id,))
    homework = c.fetchall()
    conn.close()
    return homework

def get_all_homework():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT h.id, u.full_name, u.class_level, h.subject, h.title, h.submitted_at, h.status 
                 FROM homework h JOIN users u ON h.student_id = u.id 
                 ORDER BY h.submitted_at DESC""")
    homework = c.fetchall()
    conn.close()
    return homework

def update_homework_status(homework_id, status, feedback):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE homework SET status=?, feedback=? WHERE id=?", (status, feedback, homework_id))
    conn.commit()
    conn.close()

def send_message(sender_id, receiver_id, message, is_admin_broadcast=False):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender_id, receiver_id, message, is_admin_broadcast) VALUES (?, ?, ?, ?)",
              (sender_id, receiver_id, message, is_admin_broadcast))
    conn.commit()
    conn.close()

def get_messages(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    # Get messages where user is either sender or receiver
    c.execute("""SELECT m.id, m.sender_id, m.receiver_id, m.message, m.sent_at, m.is_read, 
                        u1.username as sender_name, u2.username as receiver_name, m.is_admin_broadcast
                 FROM messages m
                 JOIN users u1 ON m.sender_id = u1.id
                 JOIN users u2 ON m.receiver_id = u2.id
                 WHERE m.sender_id=? OR m.receiver_id=?
                 ORDER BY m.sent_at DESC""", (user_id, user_id))
    messages = c.fetchall()
    
    # Mark messages as read
    c.execute("UPDATE messages SET is_read=1 WHERE receiver_id=? AND is_read=0", (user_id,))
    conn.commit()
    conn.close()
    return messages

def get_unread_message_count(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE receiver_id=? AND is_read=0", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def add_parent_info(student_id, parent_name, address, phone, email, nationality, children_in_school, debts_owed, remarks):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO parents 
                    (student_id, parent_name, address, phone, email, nationality, children_in_school, debts_owed, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (student_id, parent_name, address, phone, email, nationality, children_in_school, debts_owed, remarks))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Update if already exists
        c.execute("""UPDATE parents SET 
                    parent_name=?, address=?, phone=?, email=?, nationality=?, children_in_school=?, debts_owed=?, remarks=?
                    WHERE student_id=?""",
                    (parent_name, address, phone, email, nationality, children_in_school, debts_owed, remarks, student_id))
        conn.commit()
        return True
    finally:
        conn.close()

def get_parent_info(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM parents WHERE student_id=?", (student_id,))
    parent = c.fetchone()
    conn.close()
    return parent

def get_all_parents_info():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT p.*, u.full_name as student_name, u.class_level 
                 FROM parents p JOIN users u ON p.student_id = u.id""")
    parents = c.fetchall()
    conn.close()
    return parents

# Session state management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.chat_history = []
    st.session_state.disappearing_messages = []

# Helper functions
def display_profile_pic(profile_pic):
    if profile_pic:
        st.image(Image.open(BytesIO(profile_pic)), width=100, caption="Profile Picture")
    else:
        st.image(Image.new('RGB', (100, 100), color='gray'), width=100, caption="No Profile Picture")

def render_timetable(timetable):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = sorted(list(set([period for day, period, subject, teacher, room in timetable])))
    
    st.markdown('<h3 class="section-title">📅 Weekly Timetable</h3>', unsafe_allow_html=True)
    
    for day in days:
        day_schedule = [item for item in timetable if item[0] == day]
        if day_schedule:
            st.markdown(f"<h4>{day}</h4>", unsafe_allow_html=True)
            st.table({
                "Period": [f"Period {item[1]}" for item in day_schedule],
                "Subject": [item[2] for item in day_schedule],
                "Teacher": [item[3] for item in day_schedule],
                "Room": [item[4] for item in day_schedule]
            })

def show_disappearing_message(message, message_type="info"):
    """Show a message that disappears after 5 seconds"""
    if message_type == "success":
        msg = st.success(message)
    elif message_type == "error":
        msg = st.error(message)
    elif message_type == "warning":
        msg = st.warning(message)
    else:
        msg = st.info(message)
    
    # Add to session state to track
    st.session_state.disappearing_messages.append({
        "time": time.time(),
        "message": msg,
        "type": message_type
    })

def check_disappearing_messages():
    """Check and remove messages older than 5 seconds"""
    current_time = time.time()
    to_remove = []
    
    for i, msg in enumerate(st.session_state.disappearing_messages):
        if current_time - msg["time"] > 5:
            to_remove.append(i)
    
    # Remove from end to avoid index issues
    for i in sorted(to_remove, reverse=True):
        del st.session_state.disappearing_messages[i]

# Landing page
def show_landing_page():
    st.markdown("""
    <div class="header-container">
        <h1>Welcome to Danmay International Academy</h1>
        <p>Excellence in Education for Secondary Students</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="landing-feature">
            <div class="feature-icon">📚</div>
            <h3>Interactive Learning</h3>
            <p>Engage with our AI-powered learning assistant for personalized help with your studies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="landing-feature">
            <div class="feature-icon">📝</div>
            <h3>Homework Management</h3>
            <p>Submit assignments online and receive feedback from your teachers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="landing-feature">
            <div class="feature-icon">⏱️</div>
            <h3>Timetable Access</h3>
            <p>View your class schedule anytime, anywhere</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Login section
    st.markdown('<h3 class="section-title">Login to Your Account</h3>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "id": user[0],
                    "username": user[1],
                    "role": user[2],
                    "full_name": user[3],
                    "class_level": user[4],
                    "profile_pic": user[5]
                }
                st.rerun()
            else:
                show_disappearing_message("Invalid username or password", "error")
    
    # About school section
    st.markdown('<h3 class="section-title">About Our School</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <p><strong>🏆 Premier Secondary Education</strong></p>
        <p>Danmay International Academy is committed to providing quality education that nurtures the intellectual, moral, and social development of our students.</p>
        <p><strong>🌟 Mission:</strong> To provide a stimulating learning environment that promotes excellence in academics and character development.</p>
        <p><strong>✨ Vision:</strong> To be a leading educational institution that produces future leaders with strong moral values and academic excellence.</p>
    </div>
    """, unsafe_allow_html=True)

# Login page
if not st.session_state.logged_in:
    show_landing_page()
    st.stop()

# Check for disappearing messages
check_disappearing_messages()

# Admin Dashboard
if st.session_state.user["role"] == "admin":
    st.title("Admin Dashboard")
    menu = st.radio("Menu",["Student Management", "Homework Review", "Timetable Management", "Parent Information", "Messaging", "Admin Profile"])
    
    st.markdown(f'<div class="header-container"><h2>👨‍💼 Admin Dashboard</h2></div>', unsafe_allow_html=True)
    
    if menu == "Student Management":
        st.markdown('<h3 class="section-title">👥 Student Management</h3>', unsafe_allow_html=True)
        
        with st.expander("➕ Add New Student"):
            with st.form("add_student_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                full_name = st.text_input("Full Name")
                class_level = st.selectbox(
                    "Class Level",
                    ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
                )
                profile_pic = st.file_uploader("Profile Picture (optional)", type=["jpg", "png", "jpeg"])
                
                if st.form_submit_button("Create Student Account"):
                    if new_username and new_password and full_name:
                        pic_data = profile_pic.read() if profile_pic else None
                        if create_user(new_username, new_password, "student", full_name, class_level, pic_data):
                            show_disappearing_message(f"Student account for {full_name} created successfully!", "success")
                        else:
                            show_disappearing_message("Username already exists", "error")
                    else:
                        show_disappearing_message("Please fill in all required fields", "warning")
        
        st.markdown('<h4>📋 Student List</h4>', unsafe_allow_html=True)
        students = get_students()
        if students:
            for student in students:
                with st.expander(f"{student[2]} - {student[3]}"):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT profile_pic FROM users WHERE id=?", (student[0],))
                        pic_data = c.fetchone()[0]
                        conn.close()
                        
                        if pic_data:
                            st.image(Image.open(BytesIO(pic_data)), width=150)
                        else:
                            st.image(Image.new('RGB', (150, 150), color='gray'), width=150)
                    
                    with col2:
                        with st.form(f"update_form_{student[0]}"):
                            new_full_name = st.text_input("Full Name", value=student[2], key=f"name_{student[0]}")
                            new_class_level = st.selectbox(
                                "Class Level",
                                ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"],
                                index=["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"].index(student[3]),
                                key=f"class_{student[0]}")
                            new_profile_pic = st.file_uploader("Update Profile Picture", type=["jpg", "png", "jpeg"], key=f"pic_{student[0]}")
                            
                            if st.form_submit_button("Update Profile"):
                                pic_data = new_profile_pic.read() if new_profile_pic else pic_data
                                update_student_profile(student[0], new_full_name, new_class_level, pic_data)
                                show_disappearing_message("Profile updated successfully!", "success")
                                st.rerun()
        else:
            st.info("No students found")
    
    elif menu == "Homework Review":
        st.markdown('<h3 class="section-title">📚 Homework Submissions</h3>', unsafe_allow_html=True)
        
        homework_list = get_all_homework()
        if homework_list:
            for hw in homework_list:
                with st.container():
                    status_class = "submitted" if hw[6] == "graded" else "pending"
                    st.markdown(f"""
                    <div class="admin-card">
                        <div class="homework-title">{hw[3]}: {hw[4]}</div>
                        <div>Student: {hw[1]} (Class: {hw[2]})</div>
                        <div class="homework-due">Submitted: {hw[5]}</div>
                        <div>Status: <span class="homework-status {status_class}">{hw[6]}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Details"):
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT description, file_name, file_type, feedback FROM homework WHERE id=?", (hw[0],))
                        details = c.fetchone()
                        conn.close()
                        
                        st.write(f"**Description:** {details[0]}")
                        if details[1]:
                            st.write(f"**Attached File:** {details[1]} ({details[2]})")
                        
                        with st.form(f"feedback_form_{hw[0]}"):
                            feedback = st.text_area("Feedback", value=details[3] if details[3] else "")
                            status = st.selectbox("Status", ["pending", "graded"], index=0 if hw[6] == "pending" else 1)
                            
                            if st.form_submit_button("Update"):
                                update_homework_status(hw[0], status, feedback)
                                show_disappearing_message("Homework updated successfully!", "success")
                                st.rerun()
        else:
            st.info("No homework submissions yet")
    
    elif menu == "Timetable Management":
        st.markdown('<h3 class="section-title">⏱️ Timetable Management</h3>', unsafe_allow_html=True)
        
        with st.form("add_timetable_form"):
            col1, col2 = st.columns(2)
            with col1:
                class_level = st.selectbox(
                    "Class Level",
                    ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
                )
                day = st.selectbox(
                    "Day",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                )
            with col2:
                period = st.number_input("Period", min_value=1, max_value=8, step=1)
                subject = st.text_input("Subject")
                teacher = st.text_input("Teacher")
                room = st.text_input("Room")
            
            if st.form_submit_button("Add to Timetable"):
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("INSERT INTO timetable (class_level, day, period, subject, teacher, room) VALUES (?, ?, ?, ?, ?, ?)",
                          (class_level, day, period, subject, teacher, room))
                conn.commit()
                conn.close()
                show_disappearing_message("Timetable entry added successfully!", "success")
        
        st.markdown('<h4>Current Timetable</h4>', unsafe_allow_html=True)
        selected_class = st.selectbox(
            "View Timetable for Class",
            ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
        )
        timetable = get_timetable(selected_class)
        render_timetable(timetable)
    
    elif menu == "Parent Information":
        st.markdown('<h3 class="section-title">👪 Parent Information</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Add/Edit Parent Info", "View All Parents"])
        
        with tab1:
            student_id = st.selectbox(
                "Select Student",
                [f"{s[0]} - {s[2]} ({s[3]})" for s in get_students()],
                index=None,
                placeholder="Select a student"
            )
            
            if student_id:
                student_id = int(student_id.split(" - ")[0])
                existing_info = get_parent_info(student_id)
                
                with st.form("parent_info_form"):
                    parent_name = st.text_input("Parent Name", value=existing_info[2] if existing_info else "")
                    address = st.text_area("Address", value=existing_info[3] if existing_info else "")
                    phone = st.text_input("Phone Number", value=existing_info[4] if existing_info else "")
                    email = st.text_input("Email", value=existing_info[5] if existing_info else "")
                    nationality = st.text_input("Nationality", value=existing_info[6] if existing_info else "")
                    children_in_school = st.number_input("Number of Children in School", min_value=1, value=existing_info[7] if existing_info else 1)
                    debts_owed = st.number_input("Debts Owed", min_value=0.0, value=float(existing_info[8]) if existing_info else 0.0)
                    remarks = st.text_area("Remarks", value=existing_info[9] if existing_info else "")
                    
                    if st.form_submit_button("Save Parent Information"):
                        if add_parent_info(student_id, parent_name, address, phone, email, nationality, children_in_school, debts_owed, remarks):
                            show_disappearing_message("Parent information saved successfully!", "success")
                        else:
                            show_disappearing_message("Error saving parent information", "error")
        
        with tab2:
            parents_info = get_all_parents_info()
            if parents_info:
                for parent in parents_info:
                    with st.expander(f"{parent[10]} - {parent[11]}"):
                        st.markdown(f"""
                        <div class="parent-card">
                            <p><strong>Parent Name:</strong> {parent[2]}</p>
                            <p><strong>Address:</strong> {parent[3]}</p>
                            <p><strong>Phone:</strong> {parent[4]}</p>
                            <p><strong>Email:</strong> {parent[5]}</p>
                            <p><strong>Nationality:</strong> {parent[6]}</p>
                            <p><strong>Children in School:</strong> {parent[7]}</p>
                            <p><strong>Debts Owed:</strong> ₦{parent[8]:,.2f}</p>
                            <p><strong>Remarks:</strong> {parent[9]}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No parent information available")
    
    elif menu == "Messaging":
        st.markdown('<h3 class="section-title">✉️ Messaging</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Send Message", "Message Inbox"])
        
        with tab1:
            with st.form("message_form"):
                message_type = st.radio("Message Type", ["To Individual Student", "To All Students"])
                
                if message_type == "To Individual Student":
                    student = st.selectbox(
                        "Select Student",
                        [f"{s[0]} - {s[2]} ({s[3]})" for s in get_students()],
                        index=None,
                        placeholder="Select a student"
                    )
                    receiver_id = int(student.split(" - ")[0]) if student else None
                    is_broadcast = False
                else:
                    st.info("This message will be sent to all students")
                    receiver_id = None  # Will be handled in the send logic
                    is_broadcast = True
                
                message = st.text_area("Message")
                
                if st.form_submit_button("Send Message"):
                    if message:
                        if message_type == "To Individual Student" and receiver_id:
                            send_message(st.session_state.user["id"], receiver_id, message)
                            show_disappearing_message("Message sent successfully!", "success")
                        elif message_type == "To All Students":
                            students = get_students()
                            for student in students:
                                send_message(st.session_state.user["id"], student[0], message, True)
                            show_disappearing_message(f"Message sent to {len(students)} students!", "success")
                    else:
                        show_disappearing_message("Please enter a message", "warning")
        
        with tab2:
            messages = get_messages(st.session_state.user["id"])
            if messages:
                for msg in messages:
                    if msg[1] == st.session_state.user["id"]:  # Sent message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div class="message-bubble student-message">
                                <div><strong>To:</strong> {msg[7]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem; text-align: right;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # Received message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div class="message-bubble admin-message">
                                <div><strong>From:</strong> {msg[6]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No messages yet")
    
    elif menu == "Admin Profile":
        st.markdown('<h3 class="section-title">👤 Admin Profile</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <h4>{st.session_state.user['full_name']}</h4>
                <p>Administrator</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("logout_form"):
            if st.form_submit_button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()

# Student Dashboard
else:
    st.title("Student Dashboard")
    menu = st.radio("Menu",["Learning Assistant", "Homework", "Timetable", "Messages", "My Profile"])
    
    # Display student profile in sidebar
    with st.sidebar:
        if st.session_state.user["profile_pic"]:
            st.image(Image.open(BytesIO(st.session_state.user["profile_pic"])), width=100, caption=st.session_state.user["full_name"])
        else:
            st.image(Image.new('RGB', (100, 100), color='gray'), width=100, caption=st.session_state.user["full_name"])
        st.markdown(f"**Class:** {st.session_state.user['class_level']}")
        
        # Show unread message count
        unread_count = get_unread_message_count(st.session_state.user["id"])
        if unread_count > 0:
            st.markdown(f"**Unread Messages:** {unread_count}")
        
        with st.form("logout_form"):
            if st.form_submit_button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
    
    if menu == "Learning Assistant":
        st.markdown(f'<div class="header-container"><h2>📚 Learning Assistant</h2></div>', unsafe_allow_html=True)
        
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
                    "content": f"""You are Danmay International Academy's educational assistant for a secondary student in {st.session_state.user['class_level']}.
                    
                    STRICT RULES:
                    1. ONLY respond to educational questions related to school subjects, homework, or school activities
                    2. For non-educational questions, respond: "I'm sorry, I can only assist with educational matters. Please ask about your school work or subjects."
                    3. Maintain a professional, encouraging tone suitable for secondary students
                    4. Adapt explanations to {st.session_state.user['class_level']} level
                    5. Never provide personal opinions or non-educational advice
                    
                    Current Subjects (adjust based on class level):
                    - JSS: English, Mathematics, Basic Science, Social Studies
                    - SSS: English, Mathematics, Sciences, Humanities
                    
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
    
    elif menu == "Homework":
        st.markdown(f'<div class="header-container"><h2>📝 Homework</h2></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Submit Homework", "My Submissions"])
        
        with tab1:
            with st.form("homework_form"):
                subject = st.selectbox(
                    "Subject",
                    ["English", "Mathematics", "Physics", "Chemistry", "Biology", 
                     "Geography", "Economics", "Computer Science", "Others"]
                )
                title = st.text_input("Title")
                description = st.text_area("Description")
                homework_file = st.file_uploader("Upload Homework File", type=["pdf", "docx", "txt"])
                
                if st.form_submit_button("Submit Homework"):
                    if subject and title and description:
                        file_data = homework_file.read() if homework_file else None
                        file_name = homework_file.name if homework_file else None
                        file_type = homework_file.type if homework_file else None
                        
                        submit_homework(
                            st.session_state.user["id"],
                            subject,
                            title,
                            description,
                            file_data,
                            file_name,
                            file_type
                        )
                        show_disappearing_message("Homework submitted successfully!", "success")
                    else:
                        show_disappearing_message("Please fill in all required fields", "warning")
        
        with tab2:
            homework_list = get_student_homework(st.session_state.user["id"])
            if homework_list:
                for hw in homework_list:
                    with st.container():
                        status_class = "submitted" if hw[6] == "graded" else "pending"
                        st.markdown(f"""
                        <div class="homework-card">
                            <div class="homework-title">{hw[1]}: {hw[2]}</div>
                            <div>{hw[3]}</div>
                            <div class="homework-due">Submitted: {hw[5]}</div>
                            <div>Status: <span class="homework-status {status_class}">{hw[6]}</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if hw[4]:  # If file exists
                            st.write(f"Attached file: {hw[4]}")
                        
                        if hw[7]:  # If feedback exists
                            st.markdown(f"**Feedback:** {hw[7]}")
            else:
                st.info("You haven't submitted any homework yet")
    
    elif menu == "Timetable":
        st.markdown(f'<div class="header-container"><h2>⏱️ My Timetable</h2></div>', unsafe_allow_html=True)
        
        timetable = get_timetable(st.session_state.user["class_level"])
        if timetable:
            render_timetable(timetable)
        else:
            st.info("Timetable not available for your class yet")
    
    elif menu == "Messages":
        st.markdown(f'<div class="header-container"><h2>✉️ Messages</h2></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Contact Admin", "My Messages"])
        
        with tab1:
            with st.form("contact_admin_form"):
                message = st.text_area("Message to Admin")
                
                if st.form_submit_button("Send Message"):
                    if message:
                        # Get admin ID
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT id FROM users WHERE role='admin' LIMIT 1")
                        admin_id = c.fetchone()[0]
                        conn.close()
                        
                        send_message(st.session_state.user["id"], admin_id, message)
                        show_disappearing_message("Message sent to admin!", "success")
                    else:
                        show_disappearing_message("Please enter a message", "warning")
        
        with tab2:
            messages = get_messages(st.session_state.user["id"])
            if messages:
                for msg in messages:
                    if msg[1] == st.session_state.user["id"]:  # Sent message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div class="message-bubble student-message">
                                <div><strong>To:</strong> Admin</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem; text-align: right;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # Received message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div class="message-bubble admin-message">
                                <div><strong>From:</strong> Admin</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem;">{msg[4]}</div>
                                {f'<div style="font-size: 0.7rem; color: #666;">(Broadcast to all students)</div>' if msg[8] else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No messages yet")
    
    elif menu == "My Profile":
        st.markdown(f'<div class="header-container"><h2>👤 My Profile</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.user["profile_pic"]:
                st.image(Image.open(BytesIO(st.session_state.user["profile_pic"])), width=150, caption="Current Profile Picture")
            else:
                st.image(Image.new('RGB', (150, 150), color='gray'), width=150, caption="No Profile Picture")
        
        with col2:
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <p><strong>Username:</strong> {st.session_state.user['username']}</p>
                <p><strong>Full Name:</strong> {st.session_state.user['full_name']}</p>
                <p><strong>Class:</strong> {st.session_state.user['class_level']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Students can't edit their profile - only view
        st.info("Please contact the admin if you need to update your profile information")
        
        # Show parent information if available
        parent_info = get_parent_info(st.session_state.user["id"])
        if parent_info:
            st.markdown('<h3 class="section-title">👪 Parent Information</h3>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="parent-card">
                <p><strong>Parent Name:</strong> {parent_info[2]}</p>
                <p><strong>Phone:</strong> {parent_info[4]}</p>
                <p><strong>Email:</strong> {parent_info[5]}</p>
            </div>
            """, unsafe_allow_html=True)

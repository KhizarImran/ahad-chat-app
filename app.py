import streamlit as st
import json
import os
from datetime import datetime
import time

# Configuration
USERS = {
    "khizar": {"name": "Khizar", "password": "khizar123"},
    "ahad": {"name": "Ahad", "password": "ahad123"}
}

MESSAGES_FILE = "messages.json"

def load_messages():
    """Load messages from JSON file"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_messages(messages):
    """Save messages to JSON file"""
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def add_message(username, message):
    """Add a new message to the chat"""
    messages = load_messages()
    new_message = {
        "username": username,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages.append(new_message)
    save_messages(messages)

def login_page():
    """Display login page"""
    st.title("🗨️ AhadChat")
    st.markdown("### Welcome! Please log in to start chatting")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.selectbox("Select User:", ["", "khizar", "ahad"])
            password = st.text_input("Password:", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    if username in USERS and USERS[username]["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.display_name = USERS[username]["name"]
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
                else:
                    st.error("❌ Please select a user and enter password!")
    
    # Show password hints
    with st.expander("🔑 Password Hints"):
        st.write("**Khizar's password:** khizar123")
        st.write("**Ahad's password:** ahad123")

def chat_page():
    """Display chat interface"""
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.display_name = None
            st.rerun()
    
    with col2:
        st.title(f"💬 Chat - Welcome {st.session_state.display_name}!")
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Auto-refresh every 5 seconds
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Display messages
    messages = load_messages()
    
    # Create a container for messages
    message_container = st.container()
    
    with message_container:
        if messages:
            for msg in messages[-50:]:  # Show last 50 messages
                timestamp = msg["timestamp"]
                username = msg["username"]
                message_text = msg["message"]
                display_name = USERS[username]["name"]
                
                # Different styling for current user vs other user
                if username == st.session_state.username:
                    # Current user's message (right-aligned)
                    st.markdown(f"""
                    <div style='text-align: right; margin: 10px 0;'>
                        <div style='background-color: #007ACC; color: white; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%; text-align: left;'>
                            <strong>You</strong><br>
                            {message_text}
                        </div>
                        <div style='font-size: 12px; color: #666; margin-top: 5px;'>
                            {timestamp}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Other user's message (left-aligned)
                    st.markdown(f"""
                    <div style='text-align: left; margin: 10px 0;'>
                        <div style='background-color: #E8E8E8; color: black; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;'>
                            <strong>{display_name}</strong><br>
                            {message_text}
                        </div>
                        <div style='font-size: 12px; color: #666; margin-top: 5px;'>
                            {timestamp}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No messages yet. Start the conversation!")
    
    # Message input form
    st.markdown("---")
    with st.form("message_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            new_message = st.text_input("Type your message:", placeholder="Enter your message here...", label_visibility="collapsed")
        with col2:
            send_button = st.form_submit_button("Send 📤", use_container_width=True)
        
        if send_button and new_message.strip():
            add_message(st.session_state.username, new_message.strip())
            st.rerun()
    
    # Auto-refresh mechanism
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 5:  # Refresh every 5 seconds
        st.session_state.last_refresh = current_time
        time.sleep(0.1)  # Small delay to prevent too frequent refreshes
        st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'display_name' not in st.session_state:
        st.session_state.display_name = None
    
    # Set page config
    st.set_page_config(
        page_title="AhadChat",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Hide Streamlit menu and footer
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Route to appropriate page
    if st.session_state.logged_in:
        chat_page()
    else:
        login_page()

if __name__ == "__main__":
    main() 
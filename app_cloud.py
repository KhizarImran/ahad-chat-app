import streamlit as st
import json
import os
from datetime import datetime
import time
import requests
from urllib.parse import quote

# Configuration - can be overridden by Streamlit secrets
USERS = {
    "khizar": {"name": "Khizar", "password": "khizar123"},
    "ahad": {"name": "Ahad", "password": "ahad123"}
}

# Use GitHub Gist as a simple cloud database
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")  # Set in Streamlit Cloud secrets
GIST_ID = st.secrets.get("GIST_ID", "")  # Set in Streamlit Cloud secrets

def load_messages_cloud():
    """Load messages from GitHub Gist (cloud storage)"""
    if not GITHUB_TOKEN or not GIST_ID:
        # Fallback to session state for demo purposes
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        return st.session_state.messages
    
    try:
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(f'https://api.github.com/gists/{GIST_ID}', headers=headers)
        if response.status_code == 200:
            gist_data = response.json()
            content = gist_data['files']['messages.json']['content']
            return json.loads(content)
    except Exception as e:
        st.error(f"Error loading messages: {str(e)}")
    
    return []

def save_messages_cloud(messages):
    """Save messages to GitHub Gist (cloud storage)"""
    if not GITHUB_TOKEN or not GIST_ID:
        # Fallback to session state for demo purposes
        st.session_state.messages = messages
        return True
    
    try:
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        data = {
            'files': {
                'messages.json': {
                    'content': json.dumps(messages, ensure_ascii=False, indent=2)
                }
            }
        }
        
        response = requests.patch(f'https://api.github.com/gists/{GIST_ID}', 
                                headers=headers, 
                                data=json.dumps(data))
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error saving messages: {str(e)}")
        return False

def add_message_cloud(username, message):
    """Add a new message to the cloud storage"""
    messages = load_messages_cloud()
    new_message = {
        "username": username,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages.append(new_message)
    save_messages_cloud(messages)

def login_page():
    """Display login page"""
    st.title("🗨️ AhadChat - Cloud Edition")
    st.markdown("### Welcome! Please log in to start chatting")
    st.info("💡 This version works across different networks and devices!")
    
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
    
    # Configuration status
    with st.expander("🔧 Configuration Status"):
        if GITHUB_TOKEN and GIST_ID:
            st.success("✅ Cloud storage configured - messages will persist")
        else:
            st.warning("⚠️ Using session storage - messages reset on refresh")
            st.write("To enable cloud storage, set up GitHub Gist in Streamlit secrets")

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
    
    # Auto-refresh setup
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Display messages
    messages = load_messages_cloud()
    
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
            add_message_cloud(st.session_state.username, new_message.strip())
            st.rerun()
    
    # Auto-refresh mechanism
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 3:  # Faster refresh for cloud
        st.session_state.last_refresh = current_time
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
        page_title="AhadChat Cloud",
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
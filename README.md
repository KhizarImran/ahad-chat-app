# AhadChat 💬

A simple chat application built with Streamlit for Khizar and Ahad to communicate with each other.

## 🎯 Two Versions Available

### 📍 Local Version (`app.py`)
Perfect for same network/computer use

### 🌍 Cloud Version (`app_cloud.py`)  
**For London ↔ Newcastle chatting!** Deploy to Streamlit Cloud for global access.

## Features

- 🔐 Simple login system for two users (Khizar and Ahad)
- 💬 Real-time chat interface
- 🔄 Auto-refresh every 3-5 seconds to see new messages
- 📱 Clean and modern UI
- 💾 Messages stored persistently (JSON file locally, GitHub Gist for cloud)
- 🌍 **Cloud version works across different networks and countries**

## 🖥️ Local Setup (Same Network)

1. **Install Python** (if not already installed)
   - Download from [python.org](https://python.org)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, go to that URL manually

## 🌍 Cloud Setup (Global Access)

**For London ↔ Newcastle chatting:**

1. **Quick Deploy** (Session Storage):
   - Upload `app_cloud.py` and `requirements_cloud.txt` to GitHub
   - Deploy to [Streamlit Cloud](https://share.streamlit.io)
   - Messages reset on refresh, but works globally instantly!

2. **Full Setup** (Persistent Storage):
   - Follow the complete guide in [`DEPLOYMENT.md`](DEPLOYMENT.md)
   - Uses GitHub Gist as database for message persistence
   - Perfect for long-term conversations

**Cloud Benefits:**
- ✅ Works from anywhere in the world
- ✅ Always online (24/7)
- ✅ Mobile-friendly
- ✅ No installation needed
- ✅ Free hosting

## How to Use

### Login
- **Khizar's credentials:**
  - Username: `khizar`
  - Password: `khizar123`

- **Ahad's credentials:**
  - Username: `ahad`
  - Password: `ahad123`

### Chatting
- Once logged in, you'll see the chat interface
- Type your message in the input box at the bottom
- Click "Send 📤" or press Enter to send
- Messages will auto-refresh every 5 seconds
- Click "🔄 Refresh" for manual refresh
- Click "🚪 Logout" to return to login page

## File Structure

```
ahadchat/
├── app.py                    # Local version (same network)
├── app_cloud.py              # Cloud version (global access)
├── requirements.txt          # Dependencies for local version
├── requirements_cloud.txt    # Dependencies for cloud version
├── run_chat.bat             # Windows launcher for local version
├── README.md                # This file
├── DEPLOYMENT.md            # Cloud deployment guide
├── .streamlit/
│   └── secrets.toml         # Streamlit Cloud secrets template
└── messages.json            # Local chat storage (created automatically)
```

## Customization

You can easily customize the app by editing `app.py`:

- **Change passwords:** Modify the `USERS` dictionary
- **Add more users:** Add entries to the `USERS` dictionary
- **Change refresh rate:** Modify the time value in the auto-refresh section
- **Customize styling:** Update the HTML/CSS in the message display section

## Technical Details

- **Framework:** Streamlit
- **Data Storage:** JSON file (`messages.json`)
- **Auto-refresh:** 5-second intervals
- **Message Limit:** Shows last 50 messages for performance

## Troubleshooting

- **Port already in use:** Streamlit will automatically find another port
- **Messages not appearing:** Click the refresh button or wait for auto-refresh
- **Login issues:** Check that you're using the correct username and password

Enjoy chatting! 🎉 
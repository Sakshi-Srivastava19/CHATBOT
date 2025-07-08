import streamlit as st
from utils import get_bot_response, BOT_PERSONAS

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Chat Assistant 🤖", page_icon="💬", layout="centered")

# --- HEADER ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        background-color: ##e0f0ff;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
    }
    .stMarkdown h1 {
        color: #4B0082;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Chat Assistant")
st.markdown("Welcome! Get personalized help from different assistant types below.")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712033.png", width=100)
    st.markdown("### 👋 Select an Assistant Role")
    selected_role = st.selectbox("🧠 Assistant Persona", list(BOT_PERSONAS.keys()))
    st.markdown("---")
    st.info("💡 Tip: Choose a role that matches your need.\nE.g., 'Study Assistant' for academic help.")
# Role change detection for reset
    if "prev_role" not in st.session_state:
        st.session_state.prev_role = None

    

    # If role is changed → reset chat
    if selected_role != st.session_state.prev_role:
        st.session_state.chat_history = []
        st.session_state.prev_role = selected_role
        st.success(f"🔄 Starting a new conversation with {selected_role}...")

    st.markdown("---")
    st.info("💡 Tip: Choose a role that matches your need.\nE.g., 'Study Assistant' for academic help.")

# --- INPUT AREA ---
#st.markdown("### 💬 Chat With the Bot")
#user_input = st.text_area("✍️ Type your message here...", placeholder="Ask me anything!")

# Init chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display conversation
st.subheader("🗨️ Conversation")
for speaker, msg, role in st.session_state.chat_history:
    icon = "🧑" if speaker == "You" else "🤖"
    st.markdown(f"**{icon} {speaker} ({role}):** {msg}")
    

# New user input always at the bottom
with st.form(key="chat_input_form", clear_on_submit=True):
    user_input = st.text_input("💬 Enter your message:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user message
    st.session_state.chat_history.append(("You", user_input, selected_role))

    # Spinner while waiting for bot
    with st.spinner("🤖 Thinking..."):
        bot_reply = get_bot_response(user_input, selected_role)

    # Append bot response
    st.session_state.chat_history.append(("Bot", bot_reply, selected_role))

    st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("🛠️ Built with ❤️ By SAKSHI SRIVASTAVA")

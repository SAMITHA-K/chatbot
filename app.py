import streamlit as st
from google import genai

# -------------------------------
#   GEMINI CLIENT SETUP
# -------------------------------
api_key = st.secrets.get("gemini_api_key", "YOUR_API_KEY")
client = genai.Client(api_key=api_key)

# System prompt for context
SYSTEM_PROMPT = """You are a helpful, intelligent AI assistant.
Give clear, friendly and accurate answers.
Explain in simple language.
If the user asks coding questions, give clean code examples.
If something is unclear, ask for clarification.
Do not create harmful or unsafe content.
Keep responses short, neat and useful."""

# -------------------------------
#   STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.title("💬 Gemini Chatbot with Chat History")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input box
user_msg = st.text_input("Ask something...")

# Send button
if st.button("Send"):
    if user_msg:
        # Add user message
        st.session_state.history.append({"role": "user", "content": user_msg})

        # Prepare messages for API with system prompt
        messages = [{"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_msg}]
        for msg in st.session_state.history[1:]:  # Include previous conversation
            messages.append(msg)

        # Send to Gemini
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"Error: {str(e)}"

        # Add assistant reply
        st.session_state.history.append({"role": "model", "content": bot_reply})

# Display the conversation
st.markdown("---")
for msg in st.session_state.history:  # Display all messages
    if msg["role"] == "user":
        st.write(f"🧑 **You:** {msg['content']}")
    else:
        st.write(f"🤖 **Bot:** {msg['content']}")

# Sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.history = []
        st.rerun()

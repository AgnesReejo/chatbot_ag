import streamlit as st
from groq import Groq
import os

st.title("🤖 Chatbot")

# ---- CONFIG ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🚨 Critical fix: stop early if key is missing
if not GROQ_API_KEY:
    st.warning("GROQ_API_KEY not found. Please set it in Streamlit Secrets.")
    st.stop()

# Create client ONLY after key exists
client = Groq(api_key=GROQ_API_KEY)

# ---- MEMORY ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- DISPLAY CHAT HISTORY ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- USER INPUT ----
user_input = st.chat_input("Ask something...")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # LLM Response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

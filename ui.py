import streamlit as st
from agent import Agent

# Create agent only once
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

st.set_page_config(page_title="Agentic AI Assistant", layout="centered")

st.title("🧠 Agentic AI Assistant")
st.write("A beginner-friendly memory-based AI assistant (No paid APIs)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type something about yourself...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get agent response
    response = st.session_state.agent.respond(user_input)

    # Show agent response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

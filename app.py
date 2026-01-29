import streamlit as st
from agent import Agent
import json

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Agentic Memory Assistant",
    page_icon="🧠",
    layout="centered"
)

# ---------------- Title ----------------
st.title("🧠 Agentic Memory Assistant")
st.caption("Local • Zero-Cost • Agentic AI with Memory & Tools")

# ---------------- Session State ----------------
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent = st.session_state.agent

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Control Panel")

st.sidebar.markdown(
    """
    **Agent Features**
    - 🧠 Persistent Memory  
    - 🛠 Tool-Based Reasoning  
    - 🤖 Local LLM (TinyLlama)  
    - 📊 Confidence Scores  
    """
)

# -------- Memory Viewer Panel --------
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Memory Viewer")

memories = agent.memory.get_all()

if memories:
    for idx, m in enumerate(memories, start=1):
        st.sidebar.markdown(f"**{idx}.** {m['text']}")
else:
    st.sidebar.write("_No memory stored yet._")

# -------- Reset Button --------
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Memory & Chat", key="reset_agent"):
    agent.memory.clear()
    st.session_state.chat_history = []
    st.success("Memory and chat reset successfully!")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Built by **Sankalp Satendra Singh**")

# ---------------- Chat Display ----------------
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            # Tool badge
            if message.get("tool"):
                tool_name = message["tool"].upper()
                st.markdown(f"🛠 **Tool used: {tool_name}**")

            st.write(message["text"])
            st.markdown(f"🔎 **Confidence:** {message['confidence']}%")


# ---------------- User Input ----------------
user_input = st.chat_input("Ask me anything...")

if user_input:
    result = agent.respond(user_input)

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", result))

    st.rerun()

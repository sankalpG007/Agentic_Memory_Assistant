import streamlit as st
from agent import Agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Agentic Memory Assistant",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("🤖 Agentic Memory Assistant")

st.caption(
    "Local • Zero-Cost • Agentic AI with Memory & Tools"
)


# =========================================================
# SESSION STATE
# =========================================================

if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


agent = st.session_state.agent


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.markdown(
    """
    **Agent Features**

    - 🤖 Persistent Memory
    - 💬 Short-Term Conversation Memory
    - 🔎 Semantic FAISS Retrieval
    - 🛠️ Tool-Based Reasoning
    - 🧠 Local TinyLlama
    - 📊 Confidence Scores
    """
)


# =========================================================
# SHORT-TERM MEMORY
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("💬 Conversation Memory")

st.sidebar.write(
    f"Recent interactions: "
    f"**{agent.conversation_memory.size()}**"
)

if st.sidebar.button(
    "🧹 Clear Conversation",
    key="clear_conversation"
):
    agent.conversation_memory.clear()
    st.session_state.chat_history = []
    st.rerun()


# =========================================================
# LONG-TERM MEMORY
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Long-Term Memory")

memories = agent.memory.get_all()

if memories:
    for idx, memory in enumerate(memories, start=1):
        st.sidebar.markdown(
            f"**{idx}.** {memory['text']}"
        )
else:
    st.sidebar.write(
        "_No long-term memory stored yet._"
    )


# =========================================================
# RESET EVERYTHING
# =========================================================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🔄 Reset Memory & Chat",
    key="reset_agent"
):
    agent.memory.clear()
    agent.semantic_memory.clear()
    agent.conversation_memory.clear()

    st.session_state.chat_history = []

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.sidebar.markdown("---")

st.sidebar.write(
    "👨‍💻 Built by **Sankalp Singh**"
)


# =========================================================
# CHAT HISTORY
# =========================================================

for speaker, message in st.session_state.chat_history:

    if speaker == "user":

        with st.chat_message("user"):
            st.write(message)

    else:

        with st.chat_message("assistant"):

            if message.get("intent"):
                st.markdown(
                    f"🧭 **Intent:** "
                    f"`{message['intent']}`"
                )

            if message.get("tool"):
                st.markdown(
                    f"🛠️ **Execution:** "
                    f"`{message['tool'].upper()}`"
                )

            st.write(message["text"])

            st.markdown(
                f"🔎 **Confidence:** "
                f"{message['confidence']}%"
            )


# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Ask me anything..."
)


if user_input:

    st.session_state.chat_history.append(
        ("user", user_input)
    )

    result = agent.respond(user_input)

    st.session_state.chat_history.append(
        ("assistant", result)
    )

    st.rerun()
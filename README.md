# 🤖 Agentic Memory Assistant

A local Agentic AI assistant built with Python, LangGraph, LangChain, FAISS, Sentence Transformers, Ollama, TinyLlama, and Streamlit.

The assistant combines persistent user memory, semantic retrieval, short-term conversation memory, tool routing, and local LLM reasoning into a stateful agent workflow.

---

## 🚀 Features

### 🧠 Persistent Memory

The assistant can store user information such as:

- Personal preferences
- Learning interests
- Career goals
- Personal facts

Stored memories are persisted locally and can be retrieved later.

---

### 🔎 Semantic Memory Retrieval

The project uses:

- Sentence Transformers
- FAISS
- Semantic similarity
- Keyword matching
- Memory categories

This allows the agent to retrieve relevant memories instead of simply returning the entire memory database.

---

### 💬 Short-Term Conversation Memory

The assistant maintains recent conversation history using a bounded conversation memory.

This allows the agent to use recent interactions as context while keeping the context window controlled.

---

### 🧭 Intent Routing

The agent analyzes each user request and routes it to the appropriate execution path.

Current routes include:

```text
User Input
    │
    ▼
  Router
    │
    ├───────────────┐
    │               │
    ▼               ▼
 Memory          Tool
 Retrieval       Execution
    │               │
    │               │
    └───────┬───────┘
            │
            ▼
           LLM

The current implementation supports:

Memory retrieval
Python learning roadmap
Machine Learning roadmap
Data Science roadmap
General LLM questions
🧩 LangGraph Agent Architecture

The agent is implemented as a LangGraph workflow.

                 ┌─────────────┐
                 │ User Input  │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   Router    │
                 └──────┬──────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
              ▼         ▼         ▼
          ┌───────┐ ┌───────┐ ┌───────┐
          │Memory │ │ Tools │ │  LLM  │
          └───┬───┘ └───┬───┘ └───┬───┘
              │         │         │
              └─────────┼─────────┘
                        ▼
                 ┌─────────────┐
                 │  Response   │
                 └─────────────┘
Graph Nodes
Router Node

Determines the intent of the user's request.

Memory Node

Retrieves relevant long-term memories using semantic and keyword-based retrieval.

Tool Node

Executes predefined learning-plan tools.

LLM Node

Uses the local TinyLlama model through LangChain and Ollama.

Response Node

Combines the result from the selected execution path into the final response.

🛠️ Technology Stack
Technology	Purpose
Python	Core application
LangGraph	Agent workflow orchestration
LangChain	LLM integration
FAISS	Vector similarity search
Sentence Transformers	Text embeddings
Ollama	Local LLM runtime
TinyLlama	Local language model
Streamlit	Web interface
JSON	Local memory persistence
🧠 Memory Architecture

The project uses two forms of memory.

Long-Term Memory

Persistent user facts are stored locally.

Example:

I am learning Python
I like football
I want to become an AI engineer

These memories are embedded and indexed for retrieval.

Short-Term Memory

Recent conversations are maintained using a bounded conversation buffer.

This provides context for the current interaction without keeping an unlimited conversation history.

🛠️ Available Tools

The agent currently contains three learning tools.

Python Study Planner

Provides a structured Python learning roadmap.

Machine Learning Roadmap

Provides a Machine Learning learning sequence.

Data Science Roadmap

Provides a Data Science learning sequence.

💻 Local LLM

The project uses TinyLlama locally through Ollama.

This means the application can perform LLM inference without requiring a paid cloud API.

The local architecture is:

Application
     │
     ▼
LangChain
     │
     ▼
Ollama
     │
     ▼
TinyLlama
📁 Project Structure
agentic-memory-assistant/
│
├── agent.py
├── app.py
├── main.py
├── config.py
├── graph.py
├── router.py
│
├── memory.py
├── semantic_memory.py
├── conversation_memory.py
│
├── langchain_llm.py
├── local_llm.py
├── tools.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── tests/
│   ├── test_graph.py
│   ├── test_memory.py
│   └── test_tools.py
│
└── .streamlit/
    ├── memory.json
    └── memory.index
⚙️ Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agentic-memory-assistant
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Install Ollama

Install Ollama and pull TinyLlama:

ollama pull tinyllama

Make sure Ollama is running before launching the application.

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

🧪 Testing

The project contains tests for the main agent components.

Run:

python tests/test_graph.py
python tests/test_memory.py
python tests/test_tools.py

The tests cover:

LangGraph routing
Memory storage and retrieval
Tool execution
LLM routing
🔐 Privacy

The project is designed around local execution.

User memory is stored locally and the language model runs through Ollama on the local machine.

No external paid LLM API is required for the core application.

🎯 Project Goal

The goal of this project is to demonstrate an agent architecture that combines:

Stateful workflow orchestration
Persistent memory
Semantic retrieval
Tool execution
Conversation context
Local LLM inference

rather than implementing a simple question-answer chatbot.

👨‍💻 Author

Sankalp Singh

MCA — Artificial Intelligence & Machine Learning

📌 Current Status

The core agent workflow is implemented and tested.

Current execution flow:

User
 ↓
Router
 ↓
Memory / Tools / LLM
 ↓
Response

The project is currently prepared for local demonstration and deployment packaging.


---

# 2. Fix `.gitignore`

Open:

```text
.gitignore

Make sure it contains:

# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
venv/
.venv/
env/

# Environment variables
.env
.env.*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Python cache
.pytest_cache/

# Logs
*.log
Important

Do not ignore:

.streamlit/memory.json
.streamlit/memory.index

if you want your current demo memory to be part of the repository.

For deployment, though, we'll decide whether persistent memory should be bundled or initialized cleanly.
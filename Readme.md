🧠 Agentic Memory Assistant

Local • Zero-Cost • Explainable Agentic AI

An Agentic AI Assistant built from scratch in Python that demonstrates memory, tool usage, explainability, and UI transparency — all running locally without paid APIs.

This project focuses on agent architecture, not just LLM calls.

🚀 Key Features
🤖 Agentic Decision-Making

Rule-based reasoning (not blind LLM usage)

Decides when to use tools vs normal chat

Clear separation between logic and language

🧠 Persistent Memory

Stores important user facts in a JSON file

Prevents duplicate entries

Automatically summarizes memory on recall

🛠 Tool-Oriented Responses

The agent intelligently uses tools when required:

📘 Python Learning Roadmap

🤖 Machine Learning Roadmap

📊 Data Science Roadmap

Each tool usage is explicitly shown in the UI.

🔎 Confidence Scoring

Every response includes a confidence score (0–100%)

Based on:

memory availability

tool usage

response type

Improves transparency and trust

🖥 Web UI (Streamlit)

Chat-style interface (ChatGPT-like)

Sidebar with:

Live Memory Viewer

Reset Memory & Chat

Tool usage badges shown in chat

Fully local & fast

🤖 Local LLM Integration

Uses TinyLlama via Ollama

Runs fully offline

LLM is used only for language generation, not decisions

🧱 Tech Stack
Layer	Technology
Language	Python
Agent Logic	Rule-based
Memory	JSON (Persistent)
LLM	TinyLlama (Ollama)
UI	Streamlit
Environment	Python venv
Cost	₹0 (Free & Local)
📁 Project Structure
Agentic_Memory_Assistant/
│
├── agent.py          # Core agent logic
├── memory.py         # Persistent memory handling
├── tools.py          # Python / ML / DS tools
├── local_llm.py      # Ollama + TinyLlama wrapper
├── app.py            # Streamlit Web UI
├── main.py           # CLI version
├── memory.json       # Stored user memory
├── assets/
│   └── demo.gif      # Project demo GIF
├── requirements.txt
└── README.md

▶️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/sankalpG007/Agentic_Memory_Assistant.git
cd Agentic_Memory_Assistant

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install Ollama & TinyLlama

Download Ollama: https://ollama.com

ollama pull tinyllama

5️⃣ Run Web UI
streamlit run app.py

💬 Example Interaction
You: I want to learn Python

🛠 Tool used: PYTHON

📘 Python Learning Roadmap:
- Learn Python basics
- Practice with small programs
- Understand OOP
- Build mini projects

🔎 Confidence: 90%

You: who am i?

🛠 Tool used: MEMORY

Here’s what I remember about you:
- I like football
- I am righty and I run fast
- I want to learn Python
- I want to learn machine learning

🔎 Confidence: 75%

🎯 Learning Objectives Achieved

Understanding Agentic AI architecture

Designing tool-using agents

Implementing persistent memory

Handling low-RAM & zero-cost constraints

Prompt engineering for small local LLMs

Building transparent & explainable AI systems

Creating a production-style Web UI

🔮 Future Improvements

Semantic memory grouping (AI/ML goals combined)

Time-based memory decay

FastAPI backend

React frontend

Multi-agent collaboration

Optional cloud LLM support

🙌 Author

Sankalp Satendra Singh
MCA (AI/ML) Student
Aspiring Data Scientist / AI Engineer

GitHub: https://github.com/sankalpG007

LinkedIn:https://linkedin.com/in/sankalp-singh-48670b21a
⭐ If you found this project helpful, feel free to star the repository!

✅ STATUS: PROJECT COMPLETE

You now have a fully working, explainable, agentic AI system with UI.

This is not a toy project.
This is portfolio-grade.
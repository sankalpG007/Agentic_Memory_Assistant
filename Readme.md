# 🧠 Agentic Memory Assistant (Local, Zero-Cost)

An **Agentic AI Assistant** built from scratch using Python that can:
- remember user information persistently
- decide when to use tools (Python / ML / Data Science roadmaps)
- summarize memory intelligently
- respond using a **local LLM (TinyLlama via Ollama)**
- show a **confidence score** for every response

This project is designed as a **learning-focused, zero-cost Agentic AI system**, progressing from beginner to intermediate concepts.

---

## 🚀 Features

### 🤖 Agentic Behavior
- Rule-based decision making (no blind LLM usage)
- Tool prioritization over free chat
- State-aware responses

### 🧠 Persistent Memory
- Stores important user facts in a JSON file
- Prevents duplicate memory entries
- Summarizes memory automatically on recall

### 🛠️ Tool Usage
The agent can intelligently decide to use:
- 📘 Python Study Planner
- 🤖 Machine Learning Roadmap
- 📊 Data Science Roadmap

### 🧩 Local LLM Integration
- Uses **TinyLlama** via **Ollama**
- Fully offline & free
- LLM used only for natural language generation (not decisions)

### 📊 Confidence Score
- Every response includes a **confidence score (0–100%)**
- Based on:
  - memory availability
  - tool usage
  - response type
- Improves transparency and trust

---

## 🧱 Tech Stack

| Component | Technology |
|--------|------------|
| Language | Python |
| Agent Logic | Rule-based |
| Memory | JSON (Persistent) |
| LLM | TinyLlama (via Ollama) |
| Environment | Python venv |
| Cost | ₹0 (Free & Local) |

---

## 📁 Project Structure
agentic-memory-assistant/
│
├── agent.py # Core agent logic
├── memory.py # Persistent memory handling
├── tools.py # Python / ML / DS roadmaps
├── local_llm.py # Ollama + TinyLlama integration
├── main.py # CLI entry point
├── memory.json # Stored user memory
├── requirements.txt
└── README.md


---

## ▶️ How to Run

### 1️⃣ Clone the repo
```bash
git clone https://github.com/sankalpG007/Agentic_Memory_Assistant.git
cd Agentic_Memory_Assistant

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

Install Ollama & TinyLlama
ollama pull tinyllama

python main.py

#Learning Goals of This Project
Understand Agentic AI architecture
Learn tool-using agents
Implement persistent memory
Handle real-world constraints (low RAM, no API)
Practice prompt engineering for small LLMs
Build explainable, transparent AI systems


#Future Improvements
Semantic memory grouping (AI / ML combined goals)
Time-based memory decay
Web UI (Streamlit / React)
FastAPI backend
Optional cloud LLM integration
Multi-agent collaboration

# Author
Sankalp Satendra Singh
MCA (AI/ML) Student
Aspiring Data Scientist / AI Engineer
GitHub: https://github.com/sankalpG007
LinkedIn: https://linkedin.com/in/sankalp-singh-48670b21a
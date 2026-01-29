# memory.py
import json
import os

class Memory:
    def __init__(self, file_path=".streamlit/memory.json"):
        self.file_path = file_path
        self._ensure_dir()
        self.memories = self._load()

    def _ensure_dir(self):
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    def save(self, intent, text):
        text = text.strip()

        if any(m["text"].lower() == text.lower() for m in self.memories):
            return

        self.memories.append({
            "intent": intent,
            "text": text
        })
        self._persist()

    def _persist(self):
        with open(self.file_path, "w") as f:
            json.dump(self.memories, f, indent=2)

    def get_all(self):
        return self.memories

    def clear(self):
        self.memories = []
        self._persist()

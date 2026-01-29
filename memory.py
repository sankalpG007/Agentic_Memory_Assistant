# memory.py
import json
import os

class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        self.memories = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = json.load(f)
                # Normalize old string memories
                if data and isinstance(data[0], str):
                    return [{"intent": "user_fact", "text": t} for t in data]
                return data
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

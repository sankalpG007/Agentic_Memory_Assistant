# memory.py

import json
import os

class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        self.memories = []
        self.load()

    def load(self):
        # Load memory from file if it exists
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.memories = data.get("memories", [])
        else:
            self.memories = []

    def save_to_file(self):
        with open(self.file_path, "w") as f:
            json.dump({"memories": self.memories}, f, indent=4)

    def save(self, memory_type, text):
        memory_item = {
            "type": memory_type,
            "text": text
        }
        self.memories.append(memory_item)
        self.save_to_file()

    def get_all(self):
        return self.memories

    def clear(self):
        self.memories = []
        self.save_to_file()

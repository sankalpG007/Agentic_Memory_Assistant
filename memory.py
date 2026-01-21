# memory.py

class Memory:
    def __init__(self):
        self.memories = []

    def save(self, memory_type, text):
        self.memories.append({
            "type": memory_type,
            "text": text
        })

    def get_by_type(self, memory_type):
        return [m["text"] for m in self.memories if m["type"] == memory_type]

    def get_all(self):
        return self.memories

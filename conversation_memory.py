from collections import deque


class ConversationMemory:
    """
    Short-term memory for the current conversation.

    Stores recent user-assistant interactions so the agent
    can maintain conversational context.
    """

    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)

    def add(self, user_message, assistant_message):
        self.messages.append({
            "user": user_message,
            "assistant": assistant_message
        })

    def get_recent(self):
        return list(self.messages)

    def get_context(self):
        if not self.messages:
            return "No previous conversation."

        context = []

        for item in self.messages:
            context.append(
                f"User: {item['user']}\n"
                f"Assistant: {item['assistant']}"
            )

        return "\n\n".join(context)

    def clear(self):
        self.messages.clear()

    def size(self):
        return len(self.messages)
class ConversationMemory:

    def __init__(self):
        self.messages = []

    def add_message(self, role, text, language):
        self.messages.append({
            "role": role,
            "text": text,
            "language": language
        })

    def get_messages(self):
        return self.messages

    def get_last_user_message(self):
        for message in reversed(self.messages):
            if message["role"] == "user":
                return message
        return None

    def get_context(self, limit=6):
        return self.messages[-limit:]

    def clear(self):
        self.messages.clear()
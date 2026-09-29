class IntentResolver:

    INTENTS = {
        "return": [
            "return",
            "refund",
            "give back",
            "product back",
            "want this product back",
            "send back",
            "devolver",
            "वापस",
        ],

        "delivery": [
            "delivery",
            "shipping",
            "deliver",
            "shipment",
            "envío",
            "डिलीवरी",
        ],

        "membership": [
            "membership",
            "member",
            "premium",
            "membresía",
            "सदस्य",
        ],
    }

    def detect_intent(self, text):
        if not text:
            return "general"

        text = text.lower().strip()

        for intent, keywords in self.INTENTS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return intent

        return "general"

    def resolve(self, current_text, context):
        # First check the current message
        current_intent = self.detect_intent(current_text)

        if current_intent != "general":
            return current_intent

        # If current message is ambiguous, use previous
        # user messages to preserve conversation context.
        for message in reversed(context[:-1]):

            if message["role"] == "user":
                previous_intent = self.detect_intent(
                    message["text"]
                )

                if previous_intent != "general":
                    return previous_intent

        return "general"
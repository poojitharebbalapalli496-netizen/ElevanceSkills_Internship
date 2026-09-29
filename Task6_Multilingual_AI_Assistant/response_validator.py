class ResponseValidator:
    def __init__(self):
        self.minimum_length = 3

    def validate(self, response, intent=None, context=None):
        if response is None:
            return {
                "is_valid": False,
                "reason": "Response is empty."
            }

        response = str(response).strip()

        if not response:
            return {
                "is_valid": False,
                "reason": "Response is empty."
            }

        if len(response) < self.minimum_length:
            return {
                "is_valid": False,
                "reason": "Response is too short."
            }

        invalid_phrases = [
            "error loading",
            "traceback",
            "exception",
            "model failed",
            "translation failed",
            "unable to translate"
        ]

        response_lower = response.lower()

        for phrase in invalid_phrases:
            if phrase in response_lower:
                return {
                    "is_valid": False,
                    "reason": f"Response contains failure text: {phrase}"
                }

        # Multilingual validation keywords
        intent_keywords = {
            "return": [
                # English
                "return",
                "refund",
                "back",

                # Spanish
                "devolver",
                "devolución",
                "devolucion",

                # Hindi
                "वापस",
                "रिफंड",

                # Telugu
                "తిరిగి",
                "వాపసు"
            ],

            "delivery": [
                # English
                "delivery",
                "shipping",
                "deliver",
                "shipment",

                # Spanish
                "envío",
                "envio",
                "entrega",

                # Hindi
                "डिलीवरी",
                "शिपिंग",

                # Telugu
                "డెలివరీ",
                "షిప్పింగ్"
            ],

            "membership": [
                # English
                "membership",
                "member",
                "premium",

                # Spanish
                "membresía",
                "membresia",

                # Hindi
                "सदस्य",
                "प्रीमियम",

                # Telugu
                "సభ్యత్వం",
                "సభ్యుడు",
                "ప్రీమియం"
            ]
        }

        if intent in intent_keywords:
            keywords = intent_keywords[intent]

            if not any(keyword.lower() in response_lower for keyword in keywords):
                return {
                    "is_valid": False,
                    "reason": f"Response does not appear consistent with {intent} intent."
                }

        return {
            "is_valid": True,
            "reason": "Response passed validation."
        }
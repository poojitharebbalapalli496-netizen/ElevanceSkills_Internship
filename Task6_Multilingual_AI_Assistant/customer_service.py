class CustomerServiceKnowledge:
    """
    Customer-service knowledge and response generation
    used by the multilingual conversation engine.
    """

    KNOWLEDGE_BASE = {
        "return": {
            "response": (
                "You can return the product within 30 days "
                "of purchase."
            ),
            "source": "Return Policy",
        },

        "delivery": {
            "response": (
                "Standard delivery usually takes 3 to 5 "
                "business days. Express delivery is available "
                "within 1 to 2 business days."
            ),
            "source": "Delivery Information",
        },

        "membership": {
            "response": (
                "Premium members receive free standard shipping "
                "on all orders."
            ),
            "source": "Membership Information",
        },

        "general": {
            "response": (
                "Could you please provide more details about "
                "your question?"
            ),
            "source": "Customer Service",
        },
    }

    def get_response(self, intent):
        """
        Return a grounded customer-service response
        based on the detected intent.
        """

        if intent not in self.KNOWLEDGE_BASE:
            intent = "general"

        information = self.KNOWLEDGE_BASE[intent]

        return {
            "response": information["response"],
            "source": information["source"],
            "intent": intent,
        }
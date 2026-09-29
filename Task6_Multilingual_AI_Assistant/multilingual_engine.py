from language_detector import (
    detect_language,
    detect_languages,
    is_mixed_language
)
from translator_ct2 import MultilingualTranslator
from conversation_memory import ConversationMemory
from intent_resolver import IntentResolver
from response_validator import ResponseValidator
from customer_service import CustomerServiceKnowledge


class MultilingualConversationEngine:

    def __init__(self):
        self.translator = MultilingualTranslator()
        self.memory = ConversationMemory()
        self.intent_resolver = IntentResolver()
        self.validator = ResponseValidator()
        self.knowledge = CustomerServiceKnowledge()

    def _normalize_mixed_language(self, text, detected_languages):

        if not detected_languages:
            return text

        if len(detected_languages) == 1:
            language = detected_languages[0]

            if language == "en":
                return text

            return self.translator.translate(
                text,
                language,
                "en"
            )

        # Hindi + English
        if "hi" in detected_languages:
            return self.translator.translate(
                text,
                "hi",
                "en"
            )

        # Telugu + English
        if "te" in detected_languages:
            return self.translator.translate(
                text,
                "te",
                "en"
            )

        # Spanish + English
        normalized_text = text

        spanish_to_english = {
            "devolver": "return",
            "devolución": "return",
            "devolucion": "return",
            "producto": "product",
            "productos": "products",
            "envío": "shipping",
            "envio": "shipping",
            "entrega": "delivery",
            "quiero": "want",
            "compra": "purchase",
            "días": "days",
            "dias": "days"
        }

        for spanish_word, english_word in spanish_to_english.items():
            normalized_text = normalized_text.replace(
                spanish_word,
                english_word
            )

        return normalized_text

    def process_input(self, text):

        language = detect_language(text)
        detected_languages = detect_languages(text)
        mixed_language = is_mixed_language(text)

        english_text = self._normalize_mixed_language(
            text,
            detected_languages
        )

        self.memory.add_message(
            "user",
            text,
            language
        )

        context = self.memory.get_context()

        intent = self.intent_resolver.resolve(
            english_text,
            context
        )

        knowledge_result = self.knowledge.get_response(
            intent
        )

        return {
            "original_text": text,
            "language": language,
            "detected_languages": detected_languages,
            "is_mixed_language": mixed_language,
            "english_text": english_text,
            "intent": intent,
            "knowledge_response": knowledge_result["response"],
            "source": knowledge_result["source"],
            "context": context
        }

    def create_response(
        self,
        english_response,
        target_language,
        intent=None
    ):

        # IMPORTANT:
        # Validate the grounded English response BEFORE translation.
        source_validation = self.validator.validate(
            english_response,
            intent=intent,
            context=self.memory.get_context()
        )

        if not source_validation["is_valid"]:
            response = (
                "I do not have enough reliable information "
                "to answer that accurately."
            )

            self.memory.add_message(
                "assistant",
                response,
                "en"
            )

            return {
                "response": response,
                "validation": source_validation,
                "language": "en"
            }

        # Translate only after the source response has passed validation.
        if target_language == "unknown":
            response = english_response

        elif target_language == "en":
            response = english_response

        else:
            response = self.translator.translate(
                english_response,
                "en",
                target_language
            )

        # Basic post-translation safety checks.
        if not response or len(response.strip()) < 3:
            return {
                "response": (
                    "I do not have enough reliable information "
                    "to answer that accurately."
                ),
                "validation": {
                    "is_valid": False,
                    "reason": "Translated response is empty or too short."
                },
                "language": target_language
            }

        self.memory.add_message(
            "assistant",
            response,
            target_language
        )

        return {
            "response": response,
            "validation": {
                "is_valid": True,
                "reason": "Source response passed validation before translation."
            },
            "language": target_language
        }

    def answer(self, text):

        result = self.process_input(text)

        response_result = self.create_response(
            result["knowledge_response"],
            result["language"],
            result["intent"]
        )

        result["response"] = response_result["response"]
        result["validation"] = response_result["validation"]

        return result
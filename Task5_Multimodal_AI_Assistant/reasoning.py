from config import EVIDENCE_THRESHOLD


class ReasoningEngine:
    """Reason over questions, evidence, and conversation context."""

    INTENTS = {
        "visual_identification",
        "brand_identification",
        "model_identification",
        "technical_specification",
        "operating_system",
        "general_visual_question"
    }

    def __init__(self, evidence_threshold=EVIDENCE_THRESHOLD):
        self.evidence_threshold = evidence_threshold

    def detect_intent(self, question):
        """Identify the user's requested information type."""

        question_lower = question.lower()

        # Specific intents must be checked before
        # general visual-identification words.

        if any(
            word in question_lower
            for word in [
                "brand",
                "company",
                "manufacturer",
                "hp",
                "dell",
                "lenovo",
                "acer",
                "asus",
                "apple",
                "macbook",
                "microsoft"
            ]
        ):
            return "brand_identification"

        if any(
            word in question_lower
            for word in [
                "exact model",
                "model"
            ]
        ):
            return "model_identification"

        if any(
            word in question_lower
            for word in [
                "ram",
                "memory",
                "processor",
                "cpu",
                "storage",
                "ssd",
                "hard disk"
            ]
        ):
            return "technical_specification"

        if any(
            word in question_lower
            for word in [
                "operating system",
                "windows",
                "linux",
                "macos"
            ]
        ):
            return "operating_system"

        if any(
            word in question_lower
            for word in [
                "shown",
                "see",
                "image",
                "picture",
                "object",
                "device"
            ]
        ):
            return "visual_identification"

        return "general_visual_question"

    def _contains_reference(self, question):
        """Detect references that may require conversation context."""

        question_lower = question.lower()

        strong_references = [
            "that one",
            "this one",
            "that device",
            "this device",
            "that laptop",
            "this laptop",
            "that object",
            "this object",
            "the device",
            "the laptop",
            "the object",
            "the item",
            "its",
            "it"
        ]

        for term in strong_references:
            if term in question_lower:
                return term

        return None

    def _resolve_reference(
        self,
        question,
        conversation_context
    ):
        """Resolve conversational references."""

        reference = self._contains_reference(question)

        # No reference in the question.
        if not reference:
            return {
                "question": question,
                "status": "none",
                "reference": None
            }

        # No previous conversation.
        # The current uploaded image can be used.
        if not conversation_context:
            return {
                "question": question,
                "status": "current_image",
                "reference": reference
            }

        previous_evidence = conversation_context.get(
            "evidence",
            {}
        )

        previous_label = previous_evidence.get(
            "primary_label"
        )

        # Previous evidence can resolve the reference.
        if previous_label:
            resolved_question = (
                f"{question} "
                f"(reference: {previous_label})"
            )

            return {
                "question": resolved_question,
                "status": "resolved",
                "reference": reference
            }

        # Previous conversation exists, but it contains
        # no evidence to resolve the reference.
        return {
            "question": question,
            "status": "unclear",
            "reference": reference
        }

    def reason(
        self,
        question,
        evidence,
        conversation_context=None
    ):
        """Generate an evidence-based reasoning result."""

        reference_result = self._resolve_reference(
            question,
            conversation_context
        )

        resolved_question = reference_result[
            "question"
        ]

        reference_status = reference_result[
            "status"
        ]

        intent = self.detect_intent(
            resolved_question
        )

        confidence = evidence.get(
            "primary_confidence",
            0.0
        )

        primary_label = evidence.get(
            "primary_label"
        )

        strong_evidence = (
            confidence >= self.evidence_threshold
        )

        # If a previous conversation exists but
        # cannot resolve the reference, ask for clarification.
        if reference_status == "unclear":
            return {
                "intent": intent,
                "status": "ambiguous",
                "answer": (
                    "Could you clarify what you are "
                    "referring to?"
                ),
                "confidence": confidence,
                "reference_status": reference_status
            }

        # --------------------------------------------------
        # Visual identification
        # --------------------------------------------------

        if intent == "visual_identification":

            if strong_evidence and primary_label:
                return {
                    "intent": intent,
                    "status": "supported",
                    "answer": (
                        f"The image appears to show "
                        f"a {primary_label}."
                    ),
                    "confidence": confidence,
                    "reference_status": reference_status
                }

            return {
                "intent": intent,
                "status": "uncertain",
                "answer": (
                    "The image does not provide enough "
                    "visual evidence for a confident "
                    "identification."
                ),
                "confidence": confidence,
                "reference_status": reference_status
            }

        # --------------------------------------------------
        # Brand identification
        # --------------------------------------------------

        if intent == "brand_identification":
            return {
                "intent": intent,
                "status": "insufficient_evidence",
                "answer": (
                    "The available visual evidence does "
                    "not reliably confirm the brand."
                ),
                "confidence": confidence,
                "reference_status": reference_status
            }

        # --------------------------------------------------
        # Model identification
        # --------------------------------------------------

        if intent == "model_identification":
            return {
                "intent": intent,
                "status": "insufficient_evidence",
                "answer": (
                    "The exact device model cannot be "
                    "reliably confirmed from the available "
                    "image evidence alone."
                ),
                "confidence": confidence,
                "reference_status": reference_status
            }

        # --------------------------------------------------
        # Technical specifications
        # --------------------------------------------------

        if intent == "technical_specification":
            return {
                "intent": intent,
                "status": "insufficient_evidence",
                "answer": (
                    "The requested technical specification "
                    "cannot be reliably determined from "
                    "the available image evidence."
                ),
                "confidence": confidence,
                "reference_status": reference_status
            }

        # --------------------------------------------------
        # Operating system
        # --------------------------------------------------

        if intent == "operating_system":
            return {
                "intent": intent,
                "status": "requires_visual_confirmation",
                "answer": (
                    "A Windows-style interface may be "
                    "visible, but the exact operating system "
                    "version cannot be confirmed reliably "
                    "from the available evidence."
                ),
                "confidence": confidence,
                "reference_status": reference_status
            }

        # --------------------------------------------------
        # General visual question
        # --------------------------------------------------

        return {
            "intent": intent,
            "status": "limited_evidence",
            "answer": (
                "I can answer based on the visual evidence "
                "available, but I will avoid making claims "
                "that cannot be supported by the image."
            ),
            "confidence": confidence,
            "reference_status": reference_status
        }
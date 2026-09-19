from config import MAX_HISTORY_TURNS


class ConversationMemory:
    """Store structured conversation state."""

    def __init__(self, max_turns=MAX_HISTORY_TURNS):
        self.max_turns = max_turns
        self.history = []
        self.current_image_id = None

    def add_turn(
        self,
        user_message,
        assistant_response,
        image_id=None,
        evidence=None,
        intent=None,
        unresolved_ambiguities=None
    ):
        """Store one structured conversation turn."""

        turn = {
            "image_id": image_id,
            "user_question": user_message,
            "evidence": evidence or {},
            "intent": intent,
            "answer": assistant_response,
            "unresolved_ambiguities": (
                unresolved_ambiguities or []
            )
        }

        self.history.append(turn)

        if image_id is not None:
            self.current_image_id = image_id

        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def get_history(self):
        """Return structured conversation history."""

        return self.history

    def get_last_turn(self):
        """Return the most recent turn."""

        if not self.history:
            return None

        return self.history[-1]

    def get_context(self):
        """Build readable context for the reasoning engine."""

        if not self.history:
            return "No previous conversation."

        context = []

        for turn in self.history:
            context.append(
                f"User: {turn['user_question']}"
            )

            if turn["intent"]:
                context.append(
                    f"Intent: {turn['intent']}"
                )

            context.append(
                f"Assistant: {turn['answer']}"
            )

            ambiguities = turn[
                "unresolved_ambiguities"
            ]

            if ambiguities:
                context.append(
                    "Unresolved ambiguities: "
                    + ", ".join(ambiguities)
                )

        return "\n".join(context)

    def resolve_reference(self, question):
        """
        Resolve simple conversational references using
        the previous turn and current image.
        """

        if not self.history:
            return {
                "resolved_question": question,
                "reference_found": False,
                "reference": None,
                "context": None
            }

        question_lower = question.lower()

        reference_terms = [
            "it",
            "this",
            "that",
            "that one",
            "this one",
            "the device",
            "the laptop",
            "the object",
            "the item"
        ]

        found_reference = None

        for term in reference_terms:
            if term in question_lower:
                found_reference = term
                break

        if not found_reference:
            return {
                "resolved_question": question,
                "reference_found": False,
                "reference": None,
                "context": None
            }

        last_turn = self.get_last_turn()

        previous_evidence = last_turn.get(
            "evidence",
            {}
        )

        previous_label = previous_evidence.get(
            "primary_label"
        )

        if previous_label:
            resolved_question = (
                f"{question} "
                f"(referring to the previously identified "
                f"{previous_label})"
            )
        else:
            resolved_question = question

        return {
            "resolved_question": resolved_question,
            "reference_found": True,
            "reference": found_reference,
            "context": last_turn
        }

    def get_previous_evidence(self):
        """Return evidence from the most recent turn."""

        last_turn = self.get_last_turn()

        if not last_turn:
            return {}

        return last_turn.get(
            "evidence",
            {}
        )

    def clear(self):
        """Clear all conversation state."""

        self.history = []
        self.current_image_id = None
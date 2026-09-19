from config import EVIDENCE_THRESHOLD


class ResponseValidator:
    """Validate responses against available evidence."""

    def __init__(self, evidence_threshold=EVIDENCE_THRESHOLD):
        self.evidence_threshold = evidence_threshold

    def _has_visual_evidence(self, evidence):
        """Check whether usable visual evidence exists."""

        return bool(
            evidence.get("primary_label")
            or evidence.get("visual_labels")
            or evidence.get("caption")
        )

    def _claim_is_supported(
        self,
        answer,
        evidence,
        intent
    ):
        """Check whether the main claim has evidence support."""

        answer_lower = answer.lower()

        primary_label = str(
            evidence.get("primary_label", "")
        ).lower()

        confidence = evidence.get(
            "primary_confidence",
            0.0
        )

        # Visual identification
        if intent == "visual_identification":

            if (
                primary_label
                and primary_label in answer_lower
                and confidence >= self.evidence_threshold
            ):
                return True

            return False

        # These require explicit evidence that our
        # current visual pipeline does not reliably provide.
        if intent in [
            "brand_identification",
            "model_identification",
            "technical_specification"
        ]:
            return False

        # OS answers require explicit evidence.
        if intent == "operating_system":
            if "cannot be confirmed" in answer_lower:
                return True

            if "may be visible" in answer_lower:
                return True

            return False

        # For cautious responses, allow statements
        # that explicitly communicate evidence limits.
        uncertainty_phrases = [
            "cannot be reliably determined",
            "cannot be confirmed",
            "not enough evidence",
            "does not reliably confirm",
            "not strong enough",
            "available evidence"
        ]

        if any(
            phrase in answer_lower
            for phrase in uncertainty_phrases
        ):
            return True

        return bool(
            primary_label
            and primary_label in answer_lower
            and confidence >= self.evidence_threshold
        )

    def validate(self, reasoning_result, evidence):
        """
        Validate a reasoning result and return a
        structured validation report.
        """

        report = {
            "status": "fail",
            "valid": False,
            "reasons": [],
            "claims": [],
            "response": ""
        }

        if not reasoning_result:
            report["reasons"].append(
                "No reasoning result was provided."
            )

            report["response"] = (
                "The answer cannot be determined "
                "from the available image."
            )

            return report

        answer = reasoning_result.get(
            "answer",
            ""
        ).strip()

        intent = reasoning_result.get(
            "intent",
            "general_visual_question"
        )

        confidence = evidence.get(
            "primary_confidence",
            0.0
        )

        if not answer:
            report["reasons"].append(
                "The generated answer is empty."
            )

            report["response"] = (
                "The answer cannot be determined "
                "from the available image."
            )

            return report

        # Record the main answer as a claim.
        report["claims"].append(
            {
                "claim": answer,
                "evidence_source": (
                    "visual_evidence"
                ),
                "confidence": confidence
            }
        )

        # Check that some evidence exists.
        if not self._has_visual_evidence(evidence):

            report["reasons"].append(
                "No usable visual evidence was available."
            )

            report["response"] = (
                "The answer cannot be determined "
                "from the available image."
            )

            return report

        # Validate claim against evidence.
        supported = self._claim_is_supported(
            answer,
            evidence,
            intent
        )

        if supported:
            report["status"] = "pass"
            report["valid"] = True

            report["reasons"].append(
                "The response is supported by "
                "available visual evidence."
            )

            report["response"] = answer

            return report

        # If the reasoning itself says evidence is insufficient,
        # the response is acceptable as a warning.
        cautious_statuses = [
            "insufficient_evidence",
            "uncertain",
            "requires_visual_confirmation",
            "limited_evidence"
        ]

        if reasoning_result.get("status") in cautious_statuses:

            report["status"] = "warn"
            report["valid"] = True

            report["reasons"].append(
                "The response correctly communicates "
                "the limits of the available evidence."
            )

            report["response"] = answer

            return report

        # Unsupported claim.
        report["status"] = "fail"
        report["valid"] = False

        report["reasons"].append(
            "The answer contains a claim that cannot "
            "be mapped to sufficient visual evidence."
        )

        report["reasons"].append(
            f"Evidence confidence: {confidence:.2%}"
        )

        report["response"] = (
            "The requested information cannot be "
            "determined reliably from the image."
        )

        return report
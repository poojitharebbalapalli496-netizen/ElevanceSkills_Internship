from config import CLASSIFICATION_CONFIDENCE_THRESHOLD


class EvidenceExtractor:
    """Convert visual model outputs into structured evidence."""

    def __init__(
        self,
        confidence_threshold=CLASSIFICATION_CONFIDENCE_THRESHOLD
    ):
        self.confidence_threshold = confidence_threshold

    def extract(self, analysis_result):
        """Build structured evidence from image analysis."""

        primary = analysis_result.get(
            "primary_classification"
        )

        classifications = analysis_result.get(
            "classifications",
            []
        )

        caption = analysis_result.get(
            "caption",
            ""
        )

        evidence = {
            "caption": caption,
            "visual_labels": [],
            "primary_label": None,
            "primary_confidence": 0.0,
            "strong_visual_evidence": False
        }

        for prediction in classifications:
            evidence["visual_labels"].append(
                {
                    "label": prediction["label"],
                    "confidence": prediction["confidence"]
                }
            )

        if primary:
            evidence["primary_label"] = primary["label"]
            evidence["primary_confidence"] = (
                primary["confidence"]
            )

            evidence["strong_visual_evidence"] = (
                primary["confidence"]
                >= self.confidence_threshold
            )

        return evidence

    def build_evidence_summary(self, evidence):
        """Create a concise evidence summary for reasoning."""

        summary = []

        if evidence["primary_label"]:
            confidence = evidence["primary_confidence"]

            summary.append(
                f"Primary visual classification: "
                f"{evidence['primary_label']} "
                f"({confidence:.2%} confidence)."
            )

        if evidence["caption"]:
            summary.append(
                f"Image caption: {evidence['caption']}"
            )

        if evidence["strong_visual_evidence"]:
            summary.append(
                "The primary visual classification "
                "meets the confidence threshold."
            )
        else:
            summary.append(
                "The visual classification does not "
                "meet the confidence threshold."
            )

        return "\n".join(summary)
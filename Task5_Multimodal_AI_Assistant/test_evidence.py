from evidence import EvidenceExtractor


def create_analysis_result():
    return {
        "caption": "len len zbook x1 15 5 - inch hd laptop",
        "classifications": [
            {
                "label": "notebook",
                "confidence": 0.7718
            },
            {
                "label": "laptop",
                "confidence": 0.1524
            },
            {
                "label": "desktop computer",
                "confidence": 0.0234
            },
            {
                "label": "hand-held computer",
                "confidence": 0.0149
            },
            {
                "label": "mouse",
                "confidence": 0.0097
            }
        ],
        "primary_classification": {
            "label": "notebook",
            "confidence": 0.7718
        }
    }


def test_primary_evidence_extraction():
    extractor = EvidenceExtractor()

    evidence = extractor.extract(create_analysis_result())

    assert evidence["primary_label"] == "notebook"
    assert evidence["primary_confidence"] == 0.7718


def test_confidence_threshold_evaluation():
    extractor = EvidenceExtractor()

    evidence = extractor.extract(create_analysis_result())

    assert evidence["strong_visual_evidence"] is True


def test_visual_label_extraction():
    extractor = EvidenceExtractor()

    evidence = extractor.extract(create_analysis_result())

    assert len(evidence["visual_labels"]) == 5
    assert evidence["visual_labels"][0]["label"] == "notebook"
    assert evidence["visual_labels"][0]["confidence"] == 0.7718


def test_evidence_summary_generation():
    extractor = EvidenceExtractor()

    evidence = extractor.extract(create_analysis_result())

    summary = extractor.build_evidence_summary(evidence)

    assert isinstance(summary, str)
    assert "notebook" in summary
    assert "77.18%" in summary
    assert "confidence threshold" in summary.lower()


def test_low_confidence_evidence():
    extractor = EvidenceExtractor()

    low_confidence_result = {
        "caption": "unclear object",
        "classifications": [
            {
                "label": "notebook",
                "confidence": 0.30
            }
        ],
        "primary_classification": {
            "label": "notebook",
            "confidence": 0.30
        }
    }

    evidence = extractor.extract(low_confidence_result)

    assert evidence["primary_label"] == "notebook"
    assert evidence["primary_confidence"] == 0.30
    assert evidence["strong_visual_evidence"] is False


def test_empty_classification_result():
    extractor = EvidenceExtractor()

    result = {
        "caption": "unclear image",
        "classifications": [],
        "primary_classification": None
    }

    evidence = extractor.extract(result)

    assert evidence["primary_label"] is None
    assert evidence["primary_confidence"] == 0.0
    assert evidence["strong_visual_evidence"] is False
    assert evidence["visual_labels"] == []
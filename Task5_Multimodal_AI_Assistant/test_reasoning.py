from reasoning import ReasoningEngine


def create_evidence():
    return {
        "primary_label": "notebook",
        "primary_confidence": 0.77,
        "visual_labels": [
            {
                "label": "notebook",
                "confidence": 0.77
            }
        ]
    }


def test_visual_identification():
    engine = ReasoningEngine()

    result = engine.reason(
        "What is shown in the image?",
        create_evidence()
    )

    assert result["intent"] == "visual_identification"
    assert result["status"] == "supported"
    assert "notebook" in result["answer"].lower()


def test_follow_up_reference():
    engine = ReasoningEngine()

    context = {
        "evidence": {
            "primary_label": "notebook",
            "primary_confidence": 0.77
        },
        "intent": "visual_identification",
        "answer": "The image appears to show a notebook."
    }

    result = engine.reason(
        "What about that device?",
        create_evidence(),
        context
    )

    assert result["reference_status"] == "resolved"
    assert result["status"] == "supported"


def test_ambiguous_reference():
    engine = ReasoningEngine()

    context = {
        "evidence": {},
        "intent": "visual_identification",
        "answer": "I am not sure."
    }

    result = engine.reason(
        "What about that one?",
        create_evidence(),
        context
    )

    assert result["reference_status"] == "unclear"
    assert result["status"] == "ambiguous"
    assert "clarify" in result["answer"].lower()


def test_brand_ambiguity():
    engine = ReasoningEngine()

    result = engine.reason(
        "Is this definitely an HP laptop?",
        create_evidence()
    )

    assert result["intent"] == "brand_identification"
    assert result["status"] == "insufficient_evidence"


def test_model_ambiguity():
    engine = ReasoningEngine()

    result = engine.reason(
        "What is the exact model?",
        create_evidence()
    )

    assert result["intent"] == "model_identification"
    assert result["status"] == "insufficient_evidence"


def test_technical_specification():
    engine = ReasoningEngine()

    result = engine.reason(
        "How much RAM does it have?",
        create_evidence()
    )

    assert result["intent"] == "technical_specification"
    assert result["status"] == "insufficient_evidence"


def test_operating_system():
    engine = ReasoningEngine()

    result = engine.reason(
        "What operating system is visible?",
        create_evidence()
    )

    assert result["intent"] == "operating_system"
    assert result["status"] == "requires_visual_confirmation"


def test_low_confidence():
    engine = ReasoningEngine()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.30
    }

    result = engine.reason(
        "What is shown in the image?",
        evidence
    )

    assert result["status"] == "uncertain"
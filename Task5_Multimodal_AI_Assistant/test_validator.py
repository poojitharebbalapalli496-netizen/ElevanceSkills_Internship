from validator import ResponseValidator


def test_valid_supported_response():
    validator = ResponseValidator()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.7718
    }

    reasoning = {
        "intent": "visual_identification",
        "status": "supported",
        "answer": "The image appears to show a notebook.",
        "confidence": 0.7718
    }

    result = validator.validate(reasoning, evidence)

    assert result["valid"] is True
    assert result["status"] == "pass"
    assert "notebook" in result["response"].lower()
    assert len(result["reasons"]) > 0


def test_unsupported_brand_response_is_cautious():
    validator = ResponseValidator()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.7718
    }

    reasoning = {
        "intent": "brand_identification",
        "status": "insufficient_evidence",
        "answer": (
            "The available visual evidence does not "
            "reliably confirm the brand."
        ),
        "confidence": 0.7718
    }

    result = validator.validate(reasoning, evidence)

    assert result["valid"] is True
    assert result["status"] == "warn"
    assert "not reliably confirm" in result["response"].lower()


def test_low_confidence_response():
    validator = ResponseValidator()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.30
    }

    reasoning = {
        "intent": "visual_identification",
        "status": "uncertain",
        "answer": (
            "The image does not provide enough visual "
            "evidence for a confident identification."
        ),
        "confidence": 0.30
    }

    result = validator.validate(reasoning, evidence)

    assert result["valid"] is True
    assert result["status"] == "warn"


def test_empty_response_fails():
    validator = ResponseValidator()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.7718
    }

    reasoning = {
        "intent": "visual_identification",
        "status": "supported",
        "answer": "",
        "confidence": 0.7718
    }

    result = validator.validate(reasoning, evidence)

    assert result["valid"] is False
    assert result["status"] == "fail"
    assert "cannot be determined" in result["response"].lower()


def test_false_supported_response_fails():
    validator = ResponseValidator()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.30
    }

    reasoning = {
        "intent": "visual_identification",
        "status": "supported",
        "answer": "The image definitely shows a notebook.",
        "confidence": 0.30
    }

    result = validator.validate(reasoning, evidence)

    assert result["valid"] is False
    assert result["status"] == "fail"
    assert "cannot be determined reliably" in result["response"].lower()


def test_missing_reasoning_result_fails():
    validator = ResponseValidator()

    evidence = {
        "primary_label": "notebook",
        "primary_confidence": 0.7718
    }

    result = validator.validate(None, evidence)

    assert result["valid"] is False
    assert result["status"] == "fail"
    assert len(result["reasons"]) > 0


def test_no_visual_evidence_fails():
    validator = ResponseValidator()

    evidence = {
        "primary_label": None,
        "primary_confidence": 0.0,
        "visual_labels": [],
        "caption": ""
    }

    reasoning = {
        "intent": "visual_identification",
        "status": "supported",
        "answer": "The image appears to show a notebook.",
        "confidence": 0.0
    }

    result = validator.validate(reasoning, evidence)

    assert result["valid"] is False
    assert result["status"] == "fail"
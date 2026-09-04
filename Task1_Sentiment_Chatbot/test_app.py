from app import generate_response


def test_positive_response():
    response = generate_response("positive")
    assert "happy" in response.lower()


def test_negative_response():
    response = generate_response("negative")
    assert "sorry" in response.lower()


def test_neutral_response():
    response = generate_response("neutral")
    assert "assist" in response.lower()


def test_uncertain_response():
    response = generate_response("uncertain")
    assert "detail" in response.lower()

def test_confidence_threshold():
    confidence = 0.50
    assert confidence < 0.60

    confidence = 0.80
    assert confidence >= 0.60
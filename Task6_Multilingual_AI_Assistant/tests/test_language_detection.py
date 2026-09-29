from language_detector import (
    detect_language,
    detect_languages,
    is_mixed_language,
)


def test_english_detection():
    assert detect_language("I want to return this product.") == "en"


def test_hindi_detection():
    assert detect_language("मैं इस उत्पाद को वापस करना चाहता हूँ।") == "hi"


def test_telugu_detection():
    assert detect_language("నేను ఈ ఉత్పత్తిని తిరిగి ఇవ్వాలనుకుంటున్నాను.") == "te"


def test_spanish_detection():
    assert detect_language("Quiero devolver este producto.") == "es"


def test_mixed_english_spanish_detection():
    text = "I want to devolver this product"

    languages = detect_languages(text)

    assert "en" in languages
    assert "es" in languages
    assert is_mixed_language(text) is True
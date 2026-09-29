from translator_ct2 import MultilingualTranslator


def test_english_to_hindi_translation():
    translator = MultilingualTranslator()

    result = translator.translate(
        "You can return the product within 30 days of purchase.",
        "en",
        "hi",
    )

    assert result
    assert len(result.strip()) > 3


def test_english_to_telugu_translation():
    translator = MultilingualTranslator()

    result = translator.translate(
        "You can return the product within 30 days of purchase.",
        "en",
        "te",
    )

    assert result
    assert len(result.strip()) > 3


def test_english_to_spanish_translation():
    translator = MultilingualTranslator()

    result = translator.translate(
        "You can return the product within 30 days of purchase.",
        "en",
        "es",
    )

    assert result
    assert len(result.strip()) > 3


def test_same_language_translation():
    translator = MultilingualTranslator()

    text = "You can return the product within 30 days of purchase."

    result = translator.translate(text, "en", "en")

    assert result == text
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "es": "Spanish",
}


# Common words that are useful for detecting code-switched messages.
LANGUAGE_MARKERS = {
    "es": {
        "devolver",
        "devolución",
        "devolucion",
        "producto",
        "productos",
        "envío",
        "envio",
        "entrega",
        "quiero",
        "puede",
        "puedo",
        "cuánto",
        "cuanto",
        "días",
        "dias",
        "compra",
    },
    "en": {
        "i",
        "want",
        "this",
        "that",
        "product",
        "return",
        "refund",
        "delivery",
        "shipping",
        "purchase",
        "days",
        "can",
        "how",
        "much",
    },
}


def _get_marker_languages(text):
    """
    Detect languages using known multilingual vocabulary.
    """

    words = set(
        text.lower()
        .replace("¿", " ")
        .replace("?", " ")
        .replace("!", " ")
        .replace(",", " ")
        .replace(".", " ")
        .split()
    )

    detected = set()

    for language, markers in LANGUAGE_MARKERS.items():
        if words.intersection(markers):
            detected.add(language)

    return detected


def detect_language(text):
    """
    Detect the primary language of a message.

    Hindi and Telugu are detected using Unicode scripts.
    English and Spanish are detected using vocabulary and
    langdetect.
    """

    if not text or not text.strip():
        return "unknown"

    text = text.strip()

    # Detect Telugu script.
    telugu_chars = sum(
        1
        for char in text
        if "\u0C00" <= char <= "\u0C7F"
    )

    # Detect Devanagari script.
    hindi_chars = sum(
        1
        for char in text
        if "\u0900" <= char <= "\u097F"
    )

    if telugu_chars > 0:
        return "te"

    if hindi_chars > 0:
        return "hi"

    # Check known language vocabulary.
    marker_languages = _get_marker_languages(text)

    if len(marker_languages) == 1:
        return next(iter(marker_languages))

    # If both English and Spanish are present,
    # English is treated as the primary language when
    # it contains more English markers.
    if marker_languages == {"en", "es"}:

        words = set(
            text.lower()
            .replace("¿", " ")
            .replace("?", " ")
            .replace("!", " ")
            .replace(",", " ")
            .replace(".", " ")
            .split()
        )

        english_count = len(
            words.intersection(LANGUAGE_MARKERS["en"])
        )

        spanish_count = len(
            words.intersection(LANGUAGE_MARKERS["es"])
        )

        if spanish_count > english_count:
            return "es"

        return "en"

    # Fall back to langdetect.
    try:

        detected = detect(text)

        if detected in SUPPORTED_LANGUAGES:
            return detected

        return "en"

    except Exception:
        return "unknown"


def detect_languages(text):
    """
    Detect all identifiable supported languages.

    This method is specifically designed to recognize
    mixed-language/code-switched messages.
    """

    if not text or not text.strip():
        return []

    languages = set()

    # Detect Telugu.
    if any(
        "\u0C00" <= char <= "\u0C7F"
        for char in text
    ):
        languages.add("te")

    # Detect Hindi.
    if any(
        "\u0900" <= char <= "\u097F"
        for char in text
    ):
        languages.add("hi")

    # Detect English/Spanish vocabulary.
    marker_languages = _get_marker_languages(text)
    languages.update(marker_languages)

    # If no marker-based language was found,
    # use langdetect as a fallback.
    if not languages:

        try:

            detected = detect(text)

            if detected in SUPPORTED_LANGUAGES:
                languages.add(detected)

        except Exception:
            pass

    return sorted(languages)


def is_mixed_language(text):
    """
    Return True when two or more supported languages
    are detected in the same message.
    """

    return len(detect_languages(text)) > 1


def get_language_name(language_code):
    return SUPPORTED_LANGUAGES.get(
        language_code,
        "Unknown"
    )
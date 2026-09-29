from intent_resolver import IntentResolver


def test_return_intent_english():
    resolver = IntentResolver()

    assert resolver.detect_intent(
        "I want to return this product."
    ) == "return"


def test_return_intent_spanish():
    resolver = IntentResolver()

    assert resolver.detect_intent(
        "Quiero devolver este producto."
    ) == "return"


def test_delivery_intent():
    resolver = IntentResolver()

    assert resolver.detect_intent(
        "How long does delivery take?"
    ) == "delivery"


def test_membership_intent():
    resolver = IntentResolver()

    assert resolver.detect_intent(
        "What benefits do premium members receive?"
    ) == "membership"


def test_general_intent():
    resolver = IntentResolver()

    assert resolver.detect_intent(
        "Hello, how are you?"
    ) == "general"
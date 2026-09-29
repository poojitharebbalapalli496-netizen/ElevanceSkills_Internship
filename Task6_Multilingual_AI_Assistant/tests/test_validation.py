from response_validator import ResponseValidator


def test_valid_return_response():
    validator = ResponseValidator()

    result = validator.validate(
        "You can return the product within 30 days of purchase.",
        intent="return",
    )

    assert result["is_valid"] is True


def test_valid_delivery_response():
    validator = ResponseValidator()

    result = validator.validate(
        "Standard delivery usually takes 3 to 5 business days.",
        intent="delivery",
    )

    assert result["is_valid"] is True


def test_valid_membership_response():
    validator = ResponseValidator()

    result = validator.validate(
        "Premium members receive free standard shipping.",
        intent="membership",
    )

    assert result["is_valid"] is True


def test_empty_response_is_invalid():
    validator = ResponseValidator()

    result = validator.validate("", intent="return")

    assert result["is_valid"] is False


def test_failure_message_is_invalid():
    validator = ResponseValidator()

    result = validator.validate(
        "Error loading the translation model.",
        intent="return",
    )

    assert result["is_valid"] is False
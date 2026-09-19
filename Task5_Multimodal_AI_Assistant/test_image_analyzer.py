from pathlib import Path

from image_analyzer import ImageAnalyzer


IMAGE_PATH = Path("test_image.png")


def test_image_analyzer_output():
    assert IMAGE_PATH.exists(), (
        f"Test image not found: {IMAGE_PATH}"
    )

    analyzer = ImageAnalyzer()
    result = analyzer.analyze(str(IMAGE_PATH))

    # Check overall result structure
    assert isinstance(result, dict)

    assert "caption" in result
    assert "classifications" in result
    assert "primary_classification" in result

    # Caption should be generated
    assert isinstance(result["caption"], str)
    assert len(result["caption"].strip()) > 0

    # Classifications should contain predictions
    classifications = result["classifications"]

    assert isinstance(classifications, list)
    assert len(classifications) > 0

    # Check prediction structure
    for prediction in classifications:
        assert "label" in prediction
        assert "confidence" in prediction

        assert isinstance(prediction["label"], str)
        assert isinstance(prediction["confidence"], float)

        assert 0.0 <= prediction["confidence"] <= 1.0

    # Check primary classification
    primary = result["primary_classification"]

    assert primary is not None
    assert "label" in primary
    assert "confidence" in primary

    assert isinstance(primary["label"], str)
    assert isinstance(primary["confidence"], float)

    assert 0.0 <= primary["confidence"] <= 1.0

    print("\n===== IMAGE ANALYSIS RESULT =====")
    print("Caption:", result["caption"])
    print("\nTop classifications:")

    for prediction in classifications:
        print(
            f"- {prediction['label']}: "
            f"{prediction['confidence']:.2%}"
        )

    print("\nPrimary classification:")
    print(
        f"{primary['label']} "
        f"({primary['confidence']:.2%})"
    )
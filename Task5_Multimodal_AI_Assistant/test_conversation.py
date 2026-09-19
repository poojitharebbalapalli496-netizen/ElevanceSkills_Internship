from conversation import ConversationMemory


def test_conversation_history_and_context():
    memory = ConversationMemory(max_turns=3)

    memory.add_turn(
        "What is shown in the image?",
        "The image appears to show a laptop.",
        image_id="image_1",
        evidence={
            "primary_label": "laptop",
            "primary_confidence": 0.77
        },
        intent="visual_identification"
    )

    memory.add_turn(
        "What type of device is it?",
        "The visual evidence indicates that it is a laptop or notebook computer.",
        image_id="image_1",
        evidence={
            "primary_label": "laptop",
            "primary_confidence": 0.77
        },
        intent="visual_identification"
    )

    memory.add_turn(
        "Can you identify the exact model?",
        "The exact model cannot be reliably confirmed from the image alone.",
        image_id="image_1",
        evidence={
            "primary_label": "laptop",
            "primary_confidence": 0.77
        },
        intent="model_identification",
        unresolved_ambiguities=["exact model"]
    )

    history = memory.get_history()

    assert len(history) == 3
    assert history[0]["user_question"] == "What is shown in the image?"
    assert history[0]["answer"] == "The image appears to show a laptop."
    assert history[2]["intent"] == "model_identification"

    context = memory.get_context()

    assert "What is shown in the image?" in context
    assert "model_identification" in context


def test_conversation_max_history_limit():
    memory = ConversationMemory(max_turns=3)

    for i in range(4):
        memory.add_turn(
            f"Question {i}",
            f"Answer {i}",
            image_id="image_1",
            intent="visual_identification"
        )

    history = memory.get_history()

    assert len(history) == 3
    assert history[0]["user_question"] == "Question 1"
    assert history[-1]["user_question"] == "Question 3"


def test_last_turn_and_previous_evidence():
    memory = ConversationMemory(max_turns=3)

    memory.add_turn(
        "What is shown?",
        "It appears to be a laptop.",
        image_id="image_1",
        evidence={
            "primary_label": "laptop",
            "primary_confidence": 0.77
        },
        intent="visual_identification"
    )

    last_turn = memory.get_last_turn()
    evidence = memory.get_previous_evidence()

    assert last_turn is not None
    assert last_turn["intent"] == "visual_identification"
    assert evidence["primary_label"] == "laptop"


def test_reference_resolution():
    memory = ConversationMemory(max_turns=3)

    memory.add_turn(
        "What is shown?",
        "It appears to be a laptop.",
        image_id="image_1",
        evidence={
            "primary_label": "laptop",
            "primary_confidence": 0.77
        },
        intent="visual_identification"
    )

    result = memory.resolve_reference("What about that device?")

    assert result["reference_found"] is True
    assert result["reference"] == "that"
    assert "laptop" in result["resolved_question"].lower()


def test_clear_conversation():
    memory = ConversationMemory(max_turns=3)

    memory.add_turn(
        "What is shown?",
        "It appears to be a laptop.",
        image_id="image_1",
        intent="visual_identification"
    )

    memory.clear()

    assert len(memory.get_history()) == 0
    assert memory.current_image_id is None
    assert memory.get_last_turn() is None
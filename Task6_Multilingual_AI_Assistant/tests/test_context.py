from conversation_memory import ConversationMemory


def test_add_and_get_messages():
    memory = ConversationMemory()

    memory.add_message("user", "I want to return this product.", "en")
    memory.add_message(
        "assistant",
        "You can return the product within 30 days of purchase.",
        "en",
    )

    messages = memory.get_messages()

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_last_user_message():
    memory = ConversationMemory()

    memory.add_message("user", "I want to return this product.", "en")
    memory.add_message(
        "assistant",
        "You can return the product within 30 days of purchase.",
        "en",
    )
    memory.add_message("user", "¿Cuánto tiempo tengo?", "es")

    last_user = memory.get_last_user_message()

    assert last_user["text"] == "¿Cuánto tiempo tengo?"
    assert last_user["language"] == "es"


def test_context_limit():
    memory = ConversationMemory()

    for i in range(8):
        memory.add_message("user", f"Message {i}", "en")

    context = memory.get_context(limit=3)

    assert len(context) == 3
    assert context[0]["text"] == "Message 5"
    assert context[-1]["text"] == "Message 7"


def test_clear_memory():
    memory = ConversationMemory()

    memory.add_message("user", "I want to return this product.", "en")

    memory.clear()

    assert memory.get_messages() == []
    assert memory.get_last_user_message() is None
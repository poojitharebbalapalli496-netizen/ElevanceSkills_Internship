from transformers import pipeline

MODEL = "google/flan-t5-small"

explainer = pipeline(
    "text-generation",
    model=MODEL
)


def explain_concept(concept):
    prompt = (
        "Explain this computer science research concept simply "
        "with an example: " + concept
    )

    result = explainer(
        prompt,
        max_new_tokens=120,
        do_sample=False
    )

    return result[0]["generated_text"]


if __name__ == "__main__":
    concept = input("Enter a research concept: ")

    print("\nExplanation:")
    print(explain_concept(concept))
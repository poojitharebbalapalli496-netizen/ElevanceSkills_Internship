import spacy
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")


def extract_concepts(text):
    doc = nlp(text)

    concepts = []

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()

        if len(phrase.split()) <= 5:
            concepts.append(phrase)

    concepts = list(dict.fromkeys(concepts))

    return concepts[:10]


def create_concept_visualization(text):
    concepts = extract_concepts(text)

    if not concepts:
        return None

    values = list(range(len(concepts), 0, -1))

    output_path = "concept_visualization.png"

    plt.figure(figsize=(10, 6))
    plt.barh(concepts, values)
    plt.xlabel("Concept Importance")
    plt.ylabel("Research Concepts")
    plt.title("Research Paper Concept Visualization")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

    return output_path


if __name__ == "__main__":

    text = input("Enter research abstract: ")

    result = create_concept_visualization(text)

    if result:
        print("Visualization saved as:", result)
    else:
        print("No concepts found.")
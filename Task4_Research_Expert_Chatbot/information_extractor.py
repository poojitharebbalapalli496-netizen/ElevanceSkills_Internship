import re


def extract_information(abstract):
    text = abstract.lower()

    result = {
        "Key Concepts": [],
        "Evaluation Metrics": [],
        "Challenges": []
    }

    # Key concepts
    concepts = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural networks",
        "natural language processing",
        "computer vision",
        "reinforcement learning",
        "supervised learning",
        "unsupervised learning"
    ]

    for concept in concepts:
        if concept in text:
            result["Key Concepts"].append(concept)

    # Evaluation metrics
    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1 score",
        "f1-score",
        "auc",
        "rmse",
        "mae",
        "loss"
    ]

    for metric in metrics:
        if metric in text:
            result["Evaluation Metrics"].append(metric)

    # Challenge-related keywords
    challenge_keywords = [
        "challenge",
        "challenges",
        "limitation",
        "limitations",
        "difficult",
        "difficulty",
        "problem",
        "problems",
        "drawback",
        "drawbacks",
        "issue",
        "issues",
        "constraint",
        "constraints"
    ]

    # Extract sentences containing challenge-related words
    sentences = re.split(r'(?<=[.!?])\s+', abstract)

    for sentence in sentences:
        sentence_lower = sentence.lower()

        if any(word in sentence_lower for word in challenge_keywords):
            result["Challenges"].append(sentence.strip())

    return result


if __name__ == "__main__":

    abstract = input("Enter research abstract: ")

    result = extract_information(abstract)

    print("\nExtracted Information:")

    print("\nKey Concepts:")
    for concept in result["Key Concepts"]:
        print(" -", concept)

    print("\nEvaluation Metrics:")
    for metric in result["Evaluation Metrics"]:
        print(" -", metric)

    print("\nChallenges:")
    for challenge in result["Challenges"]:
        print(" -", challenge)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data_loader import load_medquad


class MedicalRetriever:
    def __init__(self, confidence_threshold=0.20):
        self.data = load_medquad()

        self.questions = [
            item["question"] for item in self.data
        ]

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.question_vectors = self.vectorizer.fit_transform(
            self.questions
        )

        self.confidence_threshold = confidence_threshold

    def search(self, query, top_k=3):
        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.question_vectors
        ).flatten()

        best_indices = similarities.argsort()[-top_k:][::-1]

        results = []

        for index in best_indices:
            score = float(similarities[index])

            results.append({
                "question": self.data[index]["question"],
                "answer": self.data[index]["answer"],
                "score": score
            })

        # Reject the result if the best match is not sufficiently relevant
        if results and results[0]["score"] < self.confidence_threshold:
            return []

        return results


if __name__ == "__main__":
    retriever = MedicalRetriever()

    query = input("Enter a medical question: ")

    results = retriever.search(query)

    if not results:
        print("\nNo sufficiently relevant medical answer was found.")

    else:
        print("\nTop matching results:\n")

        for result in results:
            print("Question:", result["question"])
            print("Similarity:", round(result["score"], 3))
            print("Answer:", result["answer"][:500])
            print("-" * 60)
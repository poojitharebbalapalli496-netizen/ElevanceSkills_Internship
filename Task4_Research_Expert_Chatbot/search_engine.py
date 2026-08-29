import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "data/arxiv_cs.jsonl"


def load_papers():
    papers = []
    with open(DATA_PATH, encoding="utf-8") as f:
        for line in f:
            papers.append(json.loads(line))
    return papers


def search_papers(query, top_k=5):
    papers = load_papers()

    texts = [
        paper["title"] + " " + paper["abstract"]
        for paper in papers
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)

    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).flatten()

    top_indices = scores.argsort()[-top_k:][::-1]

    results = []
    for i in top_indices:
        results.append({
            "title": papers[i]["title"],
            "abstract": papers[i]["abstract"],
            "score": round(float(scores[i]), 3)
        })

    return results


if __name__ == "__main__":
    query = input("Enter research topic: ")

    results = search_papers(query)

    print("\nTop Research Papers:\n")

    for i, paper in enumerate(results, 1):
        print(f"{i}. {paper['title']}")
        print(f"Score: {paper['score']}")
        print(f"Abstract: {paper['abstract'][:300]}...")
        print("-" * 60)
import json

def load_papers(path="data/arxiv_cs.jsonl"):
    papers = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            papers.append(json.loads(line))

    return papers


if __name__ == "__main__":
    papers = load_papers()
    print("Papers loaded:", len(papers))
    print("First paper:", papers[0]["title"])
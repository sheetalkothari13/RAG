from src.search import RAGSearch

if __name__ == "__main__":
    rag = RAGSearch()

    summary = rag.search_and_summarize(
        "What is NoSQL?",
        top_k=3
    )

    print(summary)
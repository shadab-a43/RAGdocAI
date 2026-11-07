from hybrid_search import hybrid_search


question = "What is RAG?"
results = hybrid_search(
    question,
    n_results=5,
    fetch_k=7
)

print("\nHybrid Search Results")

for result in results:
    print("\nSource:", result["source"])
    print("Page:", result["page"])
    print("RRF Score:", result["rrf_score"])
    print("Text:", result["text"])
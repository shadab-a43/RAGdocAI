from reranker import rerank_chunks

question = "What is Python used for?"

chunks = [
    {
        "text": "Python is used for web development, automation and data analysis.",
        "source": "sample2_python.pdf",
        "page": 1,
        "document_id": "python123"
    },
    {
        "text": "Databases store and manage structured information.",
        "source": "sample3_databases.pdf",
        "page": 1,
        "document_id": "database123"
    },
    {
        "text": "RAG stands for Retrieval-Augmented Generation.",
        "source": "sample.pdf",
        "page": 1,
        "document_id": "rag123"
    }
]

results = rerank_chunks(
    question,
    chunks,
    top_n=2
)

print("\nReranking Results")

for result in results:
    print("\nScore:", result["score"])
    print("Source:", result["meta"]["source"])
    print("Page:", result["meta"]["page"])
    print("Text:", result["text"])
from rag_pipeline import process_pdf
from keyword_search import keyword_search


# Step 1: Load PDF chunks
chunks = process_pdf("documents/sample.pdf")

# Step 2: Search using keywords
question = "Python programming language"

results = keyword_search(
    question,
    chunks,
    n_results=2
)

# Step 3: Display results
print("\nKeyword Search Results")

for result in results:
    print("\nSource:", result["source"])
    print("Page:", result["page"])
    print("BM25 Score:", result["bm25_score"])
    print("Text:", result["text"])
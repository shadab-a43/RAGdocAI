from rank_bm25 import BM25Okapi


def tokenize_text(text):
    """Convert text into lowercase words."""
    return text.lower().split()


def create_bm25_index(chunks):
    """Create a BM25 index from document chunks."""

    if not chunks:
        return None

    tokenized_chunks = [
        tokenize_text(chunk["text"])
        for chunk in chunks
    ]

    return BM25Okapi(tokenized_chunks)


def keyword_search(question, chunks, n_results=2):
    """Find relevant chunks using keyword search."""

    if not chunks:
        return []

    bm25 = create_bm25_index(chunks)

    question_tokens = tokenize_text(question)

    scores = bm25.get_scores(question_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )

    results = []

    for index in ranked_indices[:n_results]:
        if scores[index] > 0:
            results.append({
                **chunks[index],
                "bm25_score": float(scores[index])
            })

    return results
from flashrank import Ranker, RerankRequest


# Load reranking model
ranker = Ranker(
    model_name="ms-marco-TinyBERT-L-2-v2"
)


def rerank_chunks(question, chunks, top_n=2):
    """Rerank retrieved chunks based on question relevance."""

    if not chunks:
        return []

    passages = [
        {
            "id": index,
            "text": chunk["text"],
            "meta": chunk
        }
        for index, chunk in enumerate(chunks)
    ]

    request = RerankRequest(
        query=question,
        passages=passages
    )

    results = ranker.rerank(request)

    return results[:top_n]
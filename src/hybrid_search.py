
import chromadb

from reranker import rerank_chunks
from query_rewriter import rewrite_query

from rag_pipeline import (
    retrieve_chunks,
    COLLECTION_NAME,
    DB_PATH
)

from keyword_search import keyword_search


def hybrid_search(
    question,
    n_results=2,
    fetch_k=5,
    min_score=0.1,
    collection_name=COLLECTION_NAME,
    db_path=DB_PATH
):
    """Combine query rewriting, hybrid search and reranking."""

    # Step 1: Get all stored document chunks
    client = chromadb.PersistentClient(path=db_path)

    collection = client.get_or_create_collection(
        name=collection_name
    )

    stored_data = collection.get(
        include=["documents", "metadatas"]
    )

    chunks = []

    for index, document in enumerate(stored_data["documents"]):
        metadata = stored_data["metadatas"][index]

        chunks.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "document_id": metadata["document_id"]
        })

    if not chunks:
        return []

    # Step 2: Rewrite original question
    rewritten_question = rewrite_query(question)

    print("Rewritten Query:", rewritten_question)

    # Step 3: Semantic search
    semantic_results = retrieve_chunks(
        rewritten_question,
        n_results=fetch_k,
        collection_name=collection_name,
        db_path=db_path
    )

    # Step 4: Keyword search
    keyword_results = keyword_search(
        rewritten_question,
        chunks,
        n_results=fetch_k
    )

    # Step 5: Combine rankings using RRF
    fused_scores = {}
    result_data = {}

    rrf_k = 60

    for results in [semantic_results, keyword_results]:

        for rank, chunk in enumerate(results, start=1):

            key = (
                chunk["document_id"],
                chunk["page"],
                chunk["text"]
            )

            score = 1 / (rrf_k + rank)

            fused_scores[key] = (
                fused_scores.get(key, 0) + score
            )

            result_data[key] = chunk

    # Step 6: Sort candidates using RRF
    ranked_keys = sorted(
        fused_scores,
        key=lambda key: fused_scores[key],
        reverse=True
    )

    candidate_chunks = []

    for key in ranked_keys[:fetch_k]:

        result = result_data[key].copy()
        result["rrf_score"] = fused_scores[key]

        candidate_chunks.append(result)

    # Step 7: Rerank candidates using FlashRank
    reranked_results = rerank_chunks(
        question,
        candidate_chunks,
        top_n=n_results
    )

    # Step 8: Filter results using relevance threshold
    final_results = []

    for result in reranked_results:

        if result["score"] < min_score:
            continue

        chunk = result["meta"].copy()
        chunk["rerank_score"] = result["score"]

        final_results.append(chunk)

    return final_results

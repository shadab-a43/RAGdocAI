import chromadb

from reranker import rerank_chunks

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
    collection_name=COLLECTION_NAME,
    db_path=DB_PATH
):
    """Combine semantic and keyword search using RRF."""

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

    # Step 2: Semantic search
    semantic_results = retrieve_chunks(
        question,
        n_results=fetch_k,
        collection_name=collection_name,
        db_path=db_path
    )

    # Step 3: Keyword search
    keyword_results = keyword_search(
        question,
        chunks,
        n_results=fetch_k
    )

    # Step 4: Combine rankings using RRF
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

       # Step 5: Sort candidates using RRF
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

    # Step 6: Rerank candidates using FlashRank
    reranked_results = rerank_chunks(
        question,
        candidate_chunks,
        top_n=n_results
    )

    # Step 7: Prepare final results
    final_results = []

    for result in reranked_results:

        chunk = result["meta"].copy()
        chunk["rerank_score"] = result["score"]

        final_results.append(chunk)

    return final_results
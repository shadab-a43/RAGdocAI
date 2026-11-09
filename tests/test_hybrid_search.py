from hybrid_search import hybrid_search


def test_hybrid_search_returns_results():
    results = hybrid_search(
        "What is RAG?",
        n_results=5,
        fetch_k=7
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 5


def test_hybrid_search_result_structure():
    results = hybrid_search(
        "What is RAG?",
        n_results=5,
        fetch_k=7
    )

    for result in results:
        assert "source" in result
        assert "page" in result
        assert "rrf_score" in result
        assert "rerank_score" in result
        assert "text" in result


def test_hybrid_search_relevance():
    results = hybrid_search(
        "What is RAG?",
        n_results=5,
        fetch_k=7
    )

    assert any(
        "RAG" in result["text"]
        for result in results
    )
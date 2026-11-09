from reranker import rerank_chunks


def get_sample_chunks():
    return [
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


def test_reranker_returns_top_results():
    chunks = get_sample_chunks()

    results = rerank_chunks(
        "What is Python used for?",
        chunks,
        top_n=2
    )

    assert len(results) == 2


def test_reranker_result_structure():
    chunks = get_sample_chunks()

    results = rerank_chunks(
        "What is Python used for?",
        chunks,
        top_n=2
    )

    for result in results:
        assert "score" in result
        assert "text" in result
        assert "meta" in result
        assert "source" in result["meta"]
        assert "page" in result["meta"]


def test_reranker_relevance():
    chunks = get_sample_chunks()

    results = rerank_chunks(
        "What is Python used for?",
        chunks,
        top_n=2
    )

    assert "Python" in results[0]["text"]
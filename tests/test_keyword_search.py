from rag_pipeline import process_pdf
from keyword_search import keyword_search


def test_keyword_search_returns_results():
    chunks = process_pdf("documents/sample.pdf")

    results = keyword_search(
        "Python programming language",
        chunks,
        n_results=2
    )

    assert len(results) > 0
    assert len(results) <= 2


def test_keyword_search_result_structure():
    chunks = process_pdf("documents/sample.pdf")

    results = keyword_search(
        "Python programming language",
        chunks,
        n_results=2
    )

    for result in results:
        assert "source" in result
        assert "page" in result
        assert "bm25_score" in result
        assert "text" in result
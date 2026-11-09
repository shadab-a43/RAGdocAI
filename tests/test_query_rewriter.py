from query_rewriter import rewrite_query


def test_rewrite_query_returns_text():
    question = "What is RAG?"

    rewritten_query = rewrite_query(question)

    assert isinstance(rewritten_query, str)
    assert len(rewritten_query.strip()) > 0


def test_rewrite_query_handles_python_question():
    question = "What is Python used for?"

    rewritten_query = rewrite_query(question)

    assert isinstance(rewritten_query, str)
    assert len(rewritten_query.strip()) > 0
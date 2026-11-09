from evaluation import precision_at_k, recall_at_k


def test_precision_at_k():
    retrieved = [
        "Python is a programming language.",
        "Database stores information."
    ]

    relevant = [
        "Python is a programming language."
    ]

    score = precision_at_k(retrieved, relevant, k=2)

    assert score == 0.5


def test_recall_at_k():
    retrieved = [
        "Python is a programming language.",
        "Database stores information."
    ]

    relevant = [
        "Python is a programming language.",
        "RAG uses external documents."
    ]

    score = recall_at_k(retrieved, relevant, k=2)

    assert score == 0.5


def test_metrics_with_no_relevant_results():
    retrieved = [
        "Database stores information."
    ]

    relevant = [
        "Python is a programming language."
    ]

    precision = precision_at_k(retrieved, relevant, k=2)
    recall = recall_at_k(retrieved, relevant, k=2)

    assert precision == 0
    assert recall == 0

def precision_at_k(retrieved, relevant, k):
    """Calculate Precision@K."""

    if k <= 0:
        return 0.0

    retrieved_top_k = retrieved[:k]

    relevant_count = sum(
        1 for chunk in retrieved_top_k
        if chunk in relevant
    )

    return relevant_count / k


def recall_at_k(retrieved, relevant, k):
    """Calculate Recall@K."""

    if not relevant:
        return 0.0

    retrieved_top_k = retrieved[:k]

    relevant_count = sum(
        1 for chunk in retrieved_top_k
        if chunk in relevant
    )

    return relevant_count / len(relevant)

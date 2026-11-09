from rag_pipeline import (
    process_pdf,
    generate_embeddings,
    ingest_pdf,
    ask_question
)


def test_process_pdf():
    chunks = process_pdf("documents/sample.pdf")

    assert len(chunks) > 0

    for chunk in chunks:
        assert "text" in chunk
        assert "source" in chunk
        assert "page" in chunk


def test_generate_embeddings():
    chunks = process_pdf("documents/sample.pdf")

    embeddings = generate_embeddings(chunks)

    assert len(embeddings) == len(chunks)
    assert len(embeddings[0]) == 768


def test_ingest_pdf():
    total_stored = ingest_pdf("documents/sample.pdf")

    assert total_stored > 0


def test_ask_question():
    answer = ask_question(
        "What is RAG?",
        n_results=5
    )

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0


def test_empty_collection():
    answer = ask_question(
        "What is Python?",
        collection_name="ragdocai_empty_test"
    )

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

import ollama


def test_generate_embedding():
    text = "Python is a popular programming language."

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    embeddings = response["embeddings"]

    assert len(embeddings) == 1
    assert len(embeddings[0]) == 768


def test_embedding_values():
    text = "Python programming"

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    embedding = response["embeddings"][0]

    assert all(isinstance(value, float) for value in embedding)

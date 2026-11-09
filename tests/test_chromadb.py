import chromadb


def test_chromadb_connection():
    client = chromadb.PersistentClient(path="data/chroma_db")

    assert client is not None


def test_collection_creation():
    client = chromadb.PersistentClient(path="data/chroma_db")

    collection = client.get_or_create_collection(
        name="ragdocai_collection"
    )

    assert collection.name == "ragdocai_collection"


def test_collection_count():
    client = chromadb.PersistentClient(path="data/chroma_db")

    collection = client.get_or_create_collection(
        name="ragdocai_collection"
    )

    assert collection.count() >= 0
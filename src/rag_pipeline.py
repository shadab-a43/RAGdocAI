
import ollama
import chromadb

from document_loader import load_pdf
from text_splitter import split_text


def process_pdf(file_path, chunk_size=200, overlap=30):
    """Load a PDF and split its text into chunks."""

    # Step 1: Extract text from PDF
    text = load_pdf(file_path)

    # Step 2: Split extracted text
    chunks = split_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    # Step 3: Return chunks
    return chunks


def generate_embeddings(chunks, model="nomic-embed-text"):
    """Generate embeddings for text chunks."""

    # Step 1: Generate embeddings using Ollama
    response = ollama.embed(
        model=model,
        input=chunks
    )

    # Step 2: Return embedding vectors
    return response["embeddings"]

def store_chunks(
    chunks,
    embeddings,
    collection_name="ragdocai_collection",
    db_path="data/chroma_db"
):
    """Store text chunks and embeddings in ChromaDB."""

    # Step 1: Connect to ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    # Step 2: Get or create collection
    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Step 3: Generate chunk IDs
    new_ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Step 4: Remove outdated chunks
    existing_ids = collection.get()["ids"]

    old_ids = [
        chunk_id
        for chunk_id in existing_ids
        if chunk_id not in new_ids
    ]

    if old_ids:
        collection.delete(ids=old_ids)

    # Step 5: Store chunks and embeddings
    collection.upsert(
        ids=new_ids,
        documents=chunks,
        embeddings=embeddings
    )

    # Step 6: Return total stored records
    return collection.count()

def retrieve_chunks(
    question,
    n_results=2,
    model="nomic-embed-text",
    collection_name="ragdocai_collection",
    db_path="data/chroma_db"
):
    """Retrieve relevant chunks for a question."""

    # Step 1: Generate question embedding
    response = ollama.embed(
        model=model,
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Step 2: Connect to ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    collection = client.get_collection(
        name=collection_name
    )

    # Step 3: Search for relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    # Step 4: Return retrieved documents
    return results["documents"][0]


def generate_answer(
    question,
    context,
    model="llama3.2:3b"
):
    """Generate an answer using retrieved context."""

    # Step 1: Prepare prompt
    prompt = f"""
Answer the question using ONLY the provided context.

If the context does not contain enough information,
say that the document does not contain enough information.

Context:
{context}

Question:
{question}
"""

    # Step 2: Generate answer using Ollama
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Step 3: Return generated answer
    return response["message"]["content"]

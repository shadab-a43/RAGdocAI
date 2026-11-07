
import ollama
import chromadb
import hashlib

from pathlib import Path
from document_loader import load_pdf_pages
from text_splitter import split_pages


COLLECTION_NAME = "ragdocai_collection_v2"
DB_PATH = "data/chroma_db"


def process_pdf(file_path, chunk_size=200, overlap=30):
    """Load a PDF and create chunks with source metadata."""

    # Step 1: Load page-wise PDF data
    pages = load_pdf_pages(file_path)

    # Step 2: Split pages into metadata-aware chunks
    chunks = split_pages(
        pages,
        chunk_size=chunk_size,
        overlap=overlap
    )

    # Step 3: Create a stable document ID
    file_path = str(Path(file_path).resolve())

    document_id = hashlib.sha256(
        file_path.encode("utf-8")
    ).hexdigest()[:16]

    # Step 4: Attach document ID to every chunk
    for chunk in chunks:
        chunk["document_id"] = document_id

    return chunks


def generate_embeddings(chunks, model="nomic-embed-text"):
    """Generate embeddings for text chunks."""

    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    response = ollama.embed(
        model=model,
        input=texts
    )

    return response["embeddings"]


def store_chunks(
    chunks,
    embeddings,
    collection_name=COLLECTION_NAME,
    db_path=DB_PATH
):
    """Store chunks, embeddings and metadata in ChromaDB."""

    if not chunks:
        return 0

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count must match.")

    # Step 1: Connect to ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Step 2: Get document ID
    document_id = chunks[0]["document_id"]

    # Ensure all chunks belong to the same PDF
    if any(chunk["document_id"] != document_id for chunk in chunks):
        raise ValueError("All chunks must belong to the same PDF.")

    # Step 3: Generate unique IDs
    ids = []

    for index, chunk in enumerate(chunks):
        chunk_id = (
            f"{document_id}_p{chunk['page']}_c{index}"
        )
        ids.append(chunk_id)

    # Step 4: Find previous chunks of this PDF
    existing = collection.get(
        where={"document_id": document_id}
    )

    # Step 5: Prepare metadata
    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"],
            "document_id": chunk["document_id"]
        }
        for chunk in chunks
    ]

    # Step 6: Store or update new records
    collection.upsert(
        ids=ids,
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=metadatas
    )

    # Step 7: Remove outdated chunks after successful upsert
    obsolete_ids = [
        chunk_id
        for chunk_id in existing["ids"]
        if chunk_id not in ids
    ]

    if obsolete_ids:
        collection.delete(ids=obsolete_ids)

    return len(ids)


def ingest_pdf(file_path):
    """Process a PDF and store it in ChromaDB."""

    chunks = process_pdf(file_path)

    embeddings = generate_embeddings(chunks)

    total_stored = store_chunks(
        chunks,
        embeddings
    )

    return total_stored


def retrieve_chunks(
    question,
    n_results=2,
    model="nomic-embed-text",
    collection_name=COLLECTION_NAME,
    db_path=DB_PATH
):
    """Retrieve relevant chunks with their source metadata."""

    if n_results < 1:
        raise ValueError("n_results must be at least 1.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Connect to ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Step 2: Handle empty collection
    total_records = collection.count()

    if total_records == 0:
        return []

    # Step 3: Generate question embedding
    response = ollama.embed(
        model=model,
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Step 4: Retrieve relevant records
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(n_results, total_records)
    )

    # Step 5: Return text and metadata together
    retrieved_chunks = []

    for index, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][index]

        retrieved_chunks.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "document_id": metadata["document_id"]
        })

    return retrieved_chunks


def generate_answer(
    question,
    context,
    model="llama3.2:3b"
):
    """Generate an answer using retrieved context."""

    prompt = f"""
Answer the question using ONLY the provided context.

If the context does not contain enough information,
say that the document does not contain enough information.

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


def ask_question(
    question,
    n_results=2,
    collection_name=COLLECTION_NAME,
    db_path=DB_PATH
):
    """Retrieve relevant chunks using hybrid search and generate an answer."""

    from hybrid_search import hybrid_search

    retrieved_chunks = hybrid_search(
        question,
        n_results=n_results,
        collection_name=collection_name,
        db_path=db_path
    )

    if not retrieved_chunks:
        return "No documents are available for answering this question."

    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    answer = generate_answer(question, context)

    return answer

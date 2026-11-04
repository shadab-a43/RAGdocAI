
import chromadb
import ollama

from document_loader import load_pdf
from text_splitter import split_text


# Step 1: Load PDF text
text = load_pdf("documents/sample.pdf")

# Step 2: Split text into chunks
chunks = split_text(text, chunk_size=200, overlap=30)

# Step 3: Generate embeddings
response = ollama.embed(
    model="nomic-embed-text",
    input=chunks
)

embeddings = response["embeddings"]


# Step 4: Connect to ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(
    name="ragdocai_collection"
)


# Step 5: Store chunks and embeddings
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)


# Step 6: Display results
print("Total chunks stored:", collection.count())
print("PDF embeddings stored successfully!")

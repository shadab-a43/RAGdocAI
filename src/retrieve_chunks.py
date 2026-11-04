
import chromadb
import ollama

# Step 1: User question
question = "What is ChromaDB?"

# Step 2: Convert question into embedding
response = ollama.embed(
    model="nomic-embed-text",
    input=question
)

question_embedding = response["embeddings"][0]

# Step 3: Connect to ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_collection(
    name="ragdocai_collection"
)

# Step 4: Search for relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)

# Step 5: Display retrieved results
for i in range(len(results["ids"][0])):
    print("\nResult:", i + 1)
    print("Chunk ID:", results["ids"][0][i])
    print("Text:", results["documents"][0][i])
    print("Distance:", results["distances"][0][i])

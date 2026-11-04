
import chromadb

# Step 1: Connect to ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")

# Step 2: Get existing collection
collection = client.get_collection(
    name="ragdocai_collection"
)

# Step 3: Retrieve stored data
results = collection.get(
    include=["documents", "embeddings"]
)

# Step 4: Display results
print("Total records:", len(results["ids"]))

for i in range(len(results["ids"])):
    print("\nChunk ID:", results["ids"][i])
    print("Document:", results["documents"][i])
    print("Embedding length:", len(results["embeddings"][i]))

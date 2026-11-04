
import chromadb

# Step 1: Create a local ChromaDB client
client = chromadb.PersistentClient(path="data/chroma_db")

# Step 2: Create a collection
collection = client.get_or_create_collection(
    name="ragdocai_collection"
)

# Step 3: Display collection information
print("ChromaDB connected successfully!")
print("Collection name:", collection.name)
print("Total records:", collection.count())

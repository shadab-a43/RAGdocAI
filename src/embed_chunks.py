
from document_loader import load_pdf
from text_splitter import split_text
import ollama

# Step 1: Load text from PDF
text = load_pdf("documents/sample.pdf")

# Step 2: Split text into chunks
chunks = split_text(text, chunk_size=200, overlap=30)

# Step 3: Generate embeddings for all chunks
response = ollama.embed(
    model="nomic-embed-text",
    input=chunks
)

# Step 4: Extract embeddings
embeddings = response["embeddings"]

# Step 5: Display results
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))

for i, embedding in enumerate(embeddings):
    print(f"\nChunk {i + 1}")
    print("Embedding length:", len(embedding))
    print("First 5 values:", embedding[:5])

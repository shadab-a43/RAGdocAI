
from document_loader import load_pdf
from text_splitter import split_text

# Step 1: Read text from PDF
text = load_pdf("documents/sample.pdf")

# Step 2: Split PDF text into chunks
chunks = split_text(text, chunk_size=200, overlap=30)

# Step 3: Display results
print("Total characters:", len(text))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)


from document_loader import load_pdf
from text_splitter import split_text
from document_loader import load_pdf_pages
from text_splitter import split_pages

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

# Test page-aware chunking
pages = load_pdf_pages("documents/sample.pdf")

chunks = split_pages(pages)

print("\nPage-aware Chunking Test")
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"])
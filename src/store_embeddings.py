from pathlib import Path
import chromadb

from rag_pipeline import ingest_pdf, COLLECTION_NAME, DB_PATH


# Step 1: Find all PDF files
pdf_files = list(Path("documents").glob("*.pdf"))

# Step 2: Ingest each PDF
for file_path in pdf_files:

    total_stored = ingest_pdf(file_path)

    print("\nPDF:", file_path.name)
    print("Chunks stored:", total_stored)


# Step 3: Check total records in ChromaDB
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("\nMultiple PDF Ingestion Test")
print("Total PDFs:", len(pdf_files))
print("Total chunks in ChromaDB:", collection.count())

from rag_pipeline import (
    process_pdf,
    generate_embeddings,
    store_chunks,
    retrieve_chunks,
    generate_answer,
    ingest_pdf,
    ask_question
)


# Step 1: Process PDF
chunks = process_pdf("documents/sample.pdf")

# Step 2: Generate embeddings
embeddings = generate_embeddings(chunks)

# Step 3: Store chunks
total_stored = store_chunks(chunks, embeddings)


# Step 4: Retrieve relevant chunks
question = "What is Python?"

retrieved_chunks = retrieve_chunks(question)


# Step 5: Display retrieved text and metadata
print("Retrieved Chunks:", len(retrieved_chunks))

for index, chunk in enumerate(retrieved_chunks, start=1):

    print(f"\nChunk {index}:")
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"])


# Step 6: Prepare context
context = "\n\n".join(
    chunk["text"] for chunk in retrieved_chunks
)


# Step 7: Generate answer
answer = generate_answer(question, context)


# Step 8: Display results
print("\nPipeline Test")
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))
print("Total records stored:", total_stored)

print("\nAI Answer:")
print(answer)


# Step 9: Test document ingestion
total_stored = ingest_pdf("documents/sample.pdf")

print("\nPDF Ingestion Test")
print("Total chunks stored:", total_stored)


# Step 10: Test question answering
question = "What is RAG?"

answer = ask_question(question)

print("\nAsk Question Test")
print("Question:", question)
print("Answer:", answer)

# Empty Collection Test
print("\nEmpty Retrieval Test")

empty_question = "What is Python?"

empty_chunks = retrieve_chunks(
    empty_question,
    collection_name="ragdocai_empty_test"
)

print("Retrieved chunks:", len(empty_chunks))

empty_answer = ask_question(
    empty_question,
    collection_name="ragdocai_empty_test"
)

print("AI Answer:", empty_answer)

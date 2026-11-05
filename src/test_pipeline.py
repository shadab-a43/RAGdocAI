
from rag_pipeline import (
    process_pdf,
    generate_embeddings,
    store_chunks,
    retrieve_chunks,
    generate_answer
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

# Step 5: Prepare context
context = "\n\n".join(retrieved_chunks)

# Step 6: Generate answer
answer = generate_answer(question, context)

# Step 7: Display results
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))
print("Total records stored:", total_stored)

print("\nRetrieved chunks:", len(retrieved_chunks))
print("\nAI Answer:")
print(answer)

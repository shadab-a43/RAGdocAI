
import chromadb
import ollama

# Step 1: Connect to ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_collection(
    name="ragdocai_collection"
)

# Step 2: Keep asking questions
while True:

    question = input("\nAsk a question (type 'exit' to stop): ")

    # Stop the program
    if question.lower() == "exit":
        print("Goodbye!")
        break

    # Check for empty question
    if not question.strip():
        print("Please enter a question.")
        continue

    # Step 3: Generate question embedding
    response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Step 4: Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=2
    )

    # Step 5: Prepare context
    context = "\n\n".join(results["documents"][0])

    # Step 6: Generate answer
    prompt = f"""
Answer the question using ONLY the provided context.

If the context does not contain enough information,
say that the document does not contain enough information.

Context:
{context}

Question:
{question}
"""

    answer = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Step 7: Display answer
    print("\nAI Answer:")
    print(answer["message"]["content"])

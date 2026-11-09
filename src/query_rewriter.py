
import ollama


def rewrite_query(question):
    """Convert user question into a detailed search query."""

    prompt = f"""
    Your task is to rewrite a question for document search.

    Rules:
    1. Preserve the original meaning and intent.
    2. Never remove important keywords.
    3. Do not make the query shorter or vague.
    4. Expand abbreviations when their meaning is known.
    5. Include important concepts related to the question.
    6. Return only one clear search query.
    7. Do not answer the question.

    Example:
    Question: What is RAG?
    Search query: RAG Retrieval-Augmented Generation definition and working

    Question: What is Python used for?
    Search query: Python programming language applications and uses

    Question: {question}

    Search query:
    """

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    rewritten_query = response["message"]["content"].strip()

    if "Search query:" in rewritten_query:
        rewritten_query = rewritten_query.split("Search query:")[-1]

    return rewritten_query.strip().strip('"')

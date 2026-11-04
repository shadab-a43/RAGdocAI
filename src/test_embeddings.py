
import ollama

text = "Python is a popular programming language."

response = ollama.embed(
    model="nomic-embed-text",
    input=text
)

embedding = response["embeddings"][0]

print("Text:", text)
print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])

# RAGdocAI

A beginner-friendly, local AI-powered document question-answering system using Retrieval-Augmented Generation (RAG).

## About the Project

RAGdocAI allows users to upload their documents and ask questions about their content.

Instead of answering only from its general knowledge, the AI retrieves relevant information from uploaded documents and uses that information to generate answers.

## Main Features

- Upload and read PDF documents
- Extract text from documents
- Split documents into smaller chunks
- Convert text into embeddings
- Store embeddings in ChromaDB
- Retrieve relevant information using similarity search
- Generate answers using a local LLM
- Display answers based on document content
- Show relevant document sources

## Technology Stack

- **Language:** Python
- **LLM:** Ollama
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence Transformers
- **PDF Processing:** PyMuPDF
- **User Interface:** Streamlit

## Project Goals

- Understand how RAG works internally.
- Learn document processing and text chunking.
- Understand embeddings and vector databases.
- Build a complete RAG pipeline without relying on paid APIs.
- Explore advanced RAG techniques.

## Privacy

This project is designed for local processing using locally running AI models. Initial package and model downloads may require an internet connection.

## Project Status

<em>Currently in development.</em>

## Future Improvements

- Support for multiple document formats
- Better retrieval techniques
- Reranking and hybrid search
- Retrieval evaluation
- Improved user interface
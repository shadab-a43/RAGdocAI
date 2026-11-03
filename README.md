# RAGdocAI

A beginner-friendly, local AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

## About the Project

RAGdocAI is a local document question-answering system that allows users to upload documents and ask questions about their content.

Instead of relying only on the AI model's general knowledge, RAGdocAI retrieves relevant information from uploaded documents and uses that information to generate context-based answers.

The main goal of this project is to understand and implement the complete RAG pipeline from scratch using Python and local AI models, without depending on paid APIs.

## Main Features

- Upload and read PDF documents.
- Extract text from PDF files.
- Split documents into smaller chunks.
- Convert text chunks into numerical embeddings.
- Store embeddings in ChromaDB.
- Retrieve relevant information using similarity search.
- Generate answers using a locally running LLM.
- Display answers based on document content.
- Show relevant document sources.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Run local AI models |
| Llama 3.2 (3B) | Local language model for answer generation |
| Nomic Embed Text | Generate text embeddings |
| ChromaDB | Local vector database |
| PyMuPDF | Extract text from PDF documents |
| Streamlit | Build the user interface |
| Sentence Transformers | Embedding and retrieval experimentation |

## Project Architecture

The planned RAG pipeline:

1. **Document Loading:** Read PDF files and extract text using PyMuPDF.
2. **Text Chunking:** Divide extracted text into smaller pieces.
3. **Embeddings:** Convert text chunks into numerical vectors.
4. **Vector Storage:** Store embeddings and document chunks in ChromaDB.
5. **Retrieval:** Find relevant chunks based on the user's question.
6. **Generation:** Pass retrieved context to a local LLM using Ollama.
7. **Response:** Generate an answer based on the retrieved document information.

## Project Structure

```text
RAGdocAI/
│
├── documents/
│   └── sample.pdf
│
├── data/
│
├── src/
│   ├── document_loader.py
│   ├── test_loader.py
│   ├── text_splitter.py
│   └── test_splitter.py
│
├── .gitignore
├── .gitattributes
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd RAGdocAI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install and Run Ollama

Install Ollama and download the required local models:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Note: Model downloads are required only if the models are not already available locally.

## Project Status

**Currently in Development**

### Completed

- [x] Project environment setup.
- [x] Python virtual environment configuration.
- [x] Required Python libraries installed.
- [x] Ollama installation and local model verification.
- [x] PDF text extraction using PyMuPDF.
- [x] Basic text chunking with overlap.
- [x] PDF loading and chunking pipeline tested.

### In Progress

- [ ] Generate text embeddings using Ollama.
- [ ] Integrate ChromaDB.
- [ ] Implement document retrieval.
- [ ] Connect the local LLM with retrieved context.
- [ ] Build the complete basic RAG pipeline.

### Upcoming

- [ ] Develop a Streamlit user interface.
- [ ] Support multiple document formats.
- [ ] Display source-based answers.
- [ ] Add document management.
- [ ] Implement advanced retrieval techniques.
- [ ] Evaluate retrieval quality and answer accuracy.

## Project Goals

- Understand how Retrieval-Augmented Generation works internally.
- Learn document processing and text chunking.
- Understand embeddings and vector databases.
- Build a complete RAG pipeline from scratch.
- Use locally running AI models without paid API dependencies.
- Explore advanced RAG techniques.
- Build a practical portfolio project.

## Privacy

RAGdocAI is designed around local processing using Ollama and locally stored project data.

No paid API keys are required for the planned core functionality. Internet access may be needed initially to download Python packages and AI models.

## Future Improvements

- Support for PDF, TXT and DOCX documents.
- Improved chunking strategies.
- Hybrid search.
- Reranking.
- Query rewriting.
- Similarity threshold filtering.
- Retrieval evaluation using Precision@K and Recall@K.
- Improved user interface and user experience.

## Learning Approach

This project is being developed step by step, starting with the fundamentals of RAG before moving towards advanced techniques.

The focus is on understanding the internal working of each component rather than simply using ready-made frameworks.

---

**Project Name:** RAGdocAI  
**Language:** Python  
**Approach:** Local-first RAG  
**Status:** In Development
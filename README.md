# RAGdocAI

A beginner-friendly, local AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

## About the Project

RAGdocAI is a local document question-answering system that processes documents and allows users to ask questions about their content.

Instead of relying only on the AI model's general knowledge, RAGdocAI retrieves relevant information from documents and uses that information to generate context-based answers.

The main goal of this project is to understand and implement the complete RAG pipeline from scratch using Python and local AI models, without depending on paid APIs.

## Main Features

- [x] Load and read PDF documents.
- [x] Extract text from PDF files.
- [x] Split documents into smaller chunks with overlap.
- [x] Convert text chunks into numerical embeddings.
- [x] Store embeddings in ChromaDB.
- [x] Retrieve relevant information using semantic similarity search.
- [x] Generate answers using a locally running LLM.
- [x] Answer questions using retrieved document context.
- [x] Interactive question input through the terminal.
- [x] Ask multiple questions without restarting the program.
- [x] Handle empty user input.
- [x] Avoid generating answers when the document does not contain sufficient information.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Run local AI models |
| Llama 3.2 (3B) | Local language model for answer generation |
| Nomic Embed Text | Generate text embeddings |
| ChromaDB | Local vector database |
| PyMuPDF | Extract text from PDF documents |
| Streamlit | Build the planned user interface |
| Sentence Transformers | Embedding and retrieval experimentation |

## Project Architecture

The RAG pipeline currently implemented:

1. **Document Loading:** Read PDF files and extract text using PyMuPDF.
2. **Text Chunking:** Divide extracted text into smaller pieces with overlap.
3. **Embeddings:** Convert text chunks into numerical vectors using Nomic Embed Text.
4. **Vector Storage:** Store embeddings and document chunks in ChromaDB.
5. **Retrieval:** Find relevant chunks based on the user's question using semantic similarity search.
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
│   └── chroma_db/
│
├── src/
│   ├── document_loader.py
│   ├── test_loader.py
│   ├── text_splitter.py
│   ├── test_splitter.py
│   ├── test_embeddings.py
│   ├── embed_chunks.py
│   ├── test_chromadb.py
│   ├── store_embeddings.py
│   ├── retrieve_data.py
│   ├── retrieve_chunks.py
│   └── rag_answer.py
│
├── .gitignore
├── .gitattributes
├── requirements.txt
└── README.md
```

Note: `data/chroma_db/` contains the locally stored ChromaDB database and is not intended to be committed to GitHub.

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
- [x] Generate text embeddings using Ollama.
- [x] Verify embedding dimensions.
- [x] Integrate ChromaDB.
- [x] Store document chunks and embeddings in ChromaDB.
- [x] Verify persistent vector storage.
- [x] Implement semantic document retrieval.
- [x] Generate question embeddings.
- [x] Retrieve top relevant chunks using similarity search.
- [x] Connect the local LLM with retrieved context.
- [x] Generate context-based answers using Llama 3.2.
- [x] Implement interactive question input.
- [x] Support multiple questions in one program run.
- [x] Handle insufficient information using grounded answering.
- [x] Handle empty user input.
- [x] Test Python-related questions.
- [x] Test RAG-related questions.
- [x] Test questions whose answers are not available in the document.

### In Progress

- [ ] Improve text chunking to avoid breaking words and sentences.
- [ ] Organize the complete RAG pipeline into reusable functions.
- [ ] Build the complete and refined basic RAG pipeline.
- [ ] Add document metadata and source information.
- [ ] Support multiple documents.
- [ ] Perform final basic RAG pipeline testing.

### Upcoming

- [ ] Develop a Streamlit user interface.
- [ ] Support multiple document formats.
- [ ] Allow document uploads through the interface.
- [ ] Display source-based answers with document references.
- [ ] Add document management.
- [ ] Implement advanced retrieval techniques.
- [ ] Evaluate retrieval quality and answer accuracy.
- [ ] Add chat history.
- [ ] Improve application performance and user experience.

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

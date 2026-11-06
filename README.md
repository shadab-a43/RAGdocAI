# RAGdocAI

A beginner-friendly, local AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

## About the Project

RAGdocAI is a local document question-answering system that processes PDF documents and allows users to ask questions about their content.

Instead of relying only on the AI model's general knowledge, RAGdocAI retrieves relevant information from documents and uses that information to generate context-based answers.

The main goal of this project is to understand and implement the complete RAG pipeline from scratch using Python and local AI models, without depending on paid APIs.

## Main Features

- [x] Load and read PDF documents.
- [x] Support multiple PDF documents.
- [x] Extract text from PDF files page by page.
- [x] Split documents into smaller chunks with sentence-aware boundaries.
- [x] Implement controlled text overlap between chunks.
- [x] Prevent broken words during chunking.
- [x] Preserve document source and page metadata in chunks.
- [x] Generate unique document-specific chunk IDs.
- [x] Convert text chunks into numerical embeddings.
- [x] Store embeddings and metadata in ChromaDB.
- [x] Retrieve relevant information using semantic similarity search.
- [x] Return retrieved text with source and page information.
- [x] Generate answers using a locally running LLM.
- [x] Answer questions using retrieved document context.
- [x] Handle repeated PDF ingestion without creating duplicate records.
- [x] Update existing document chunks while preserving other documents.
- [x] Handle empty document collections during retrieval.
- [x] Handle empty user input.
- [x] Avoid generating answers when no documents are available.
- [x] Organize document processing into reusable functions.
- [x] Generate embeddings through a reusable function.
- [x] Store document chunks and embeddings through a reusable function.
- [x] Retrieve relevant chunks through a reusable function.
- [x] Generate context-based answers through a reusable function.
- [x] Connect the complete workflow through a single `ask_question()` function.

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

1. **Document Loading:** Read PDF files and extract text page by page using PyMuPDF.
2. **Text Chunking:** Divide extracted text into smaller pieces using sentence-aware chunking with controlled overlap.
3. **Metadata Preservation:** Attach document source, page number and unique document ID to every chunk.
4. **Embeddings:** Convert text chunks into numerical vectors using Nomic Embed Text.
5. **Vector Storage:** Store embeddings, document chunks and metadata in ChromaDB.
6. **Retrieval:** Find relevant chunks based on the user's question using semantic similarity search.
7. **Generation:** Pass retrieved context to a local LLM using Ollama.
8. **Response:** Generate an answer based on the retrieved document information.

The complete workflow is connected through reusable functions and tested with multiple PDF documents.

## Project Structure

```text
RAGdocAI/
│
├── documents/
│   ├── sample.pdf
│   ├── sample2_python.pdf
│   └── sample3_databases.pdf
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
│   ├── rag_answer.py
│   ├── rag_pipeline.py
│   └── test_pipeline.py
│
├── .gitignore
├── .gitattributes
├── requirements.txt
└── README.md
```

Note: `data/chroma_db/` contains the locally stored ChromaDB database and is not intended to be committed to GitHub. The private `PROJECT_CONTEXT.md` file is also excluded from GitHub.

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

### 6. Add PDF Documents

Place your PDF files inside the `documents/` directory.

The project supports multiple PDF documents.

### 7. Ingest PDF Documents

From the project root:

```bash
python src/store_embeddings.py
```

This processes all PDF files inside the `documents/` directory and stores their embeddings and metadata in ChromaDB.

### 8. Run the RAG Pipeline Test

```bash
python src/test_pipeline.py
```

## Project Status

**Currently in Development**

### Completed

- [x] Project environment setup.
- [x] Python virtual environment configuration.
- [x] Required Python libraries installed.
- [x] Ollama installation and local model verification.
- [x] PDF text extraction using PyMuPDF.
- [x] Page-wise PDF text extraction.
- [x] Basic text chunking with overlap.
- [x] Sentence-aware text chunking.
- [x] Controlled overlap between chunks.
- [x] Prevent broken words during chunking.
- [x] Preserve page metadata in text chunks.
- [x] PDF loading and chunking pipeline tested.
- [x] Generate text embeddings using Ollama.
- [x] Verify embedding dimensions.
- [x] Integrate ChromaDB.
- [x] Store document chunks and embeddings in ChromaDB.
- [x] Store source, page and document ID metadata.
- [x] Verify persistent vector storage.
- [x] Synchronize updated chunks with ChromaDB.
- [x] Generate unique document-specific chunk IDs.
- [x] Implement semantic document retrieval.
- [x] Generate question embeddings.
- [x] Retrieve top relevant chunks using similarity search.
- [x] Retrieve source and page information with relevant chunks.
- [x] Connect the local LLM with retrieved context.
- [x] Generate context-based answers using Llama 3.2.
- [x] Implement interactive question input.
- [x] Support multiple questions in one program run.
- [x] Handle insufficient information using grounded answering.
- [x] Handle empty user input.
- [x] Handle empty document collections during retrieval.
- [x] Test Python-related questions.
- [x] Test RAG-related questions.
- [x] Test questions whose answers are not available in the document.
- [x] Implement reusable PDF processing function.
- [x] Implement reusable embedding generation function.
- [x] Implement reusable ChromaDB storage function.
- [x] Implement reusable retrieval function.
- [x] Implement reusable answer-generation function.
- [x] Connect the complete workflow through `ask_question()`.
- [x] Support multiple PDF documents.
- [x] Test ingestion of multiple PDFs.
- [x] Verify repeated ingestion without duplicate records.
- [x] Verify existing documents remain stored when another PDF is ingested.
- [x] Test source and page metadata retrieval.
- [x] Test empty retrieval handling.
- [x] Test the complete RAG pipeline.

### In Progress

- [ ] Improve answer responses with explicit source references and page citations.
- [ ] Organize and clean up the project for the next development stage.

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

No paid API keys are required for the core functionality. Internet access may be needed initially to download Python packages and AI models.

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
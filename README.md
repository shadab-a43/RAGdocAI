# RAGdocAI

A beginner-friendly, local AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

## About the Project

RAGdocAI is a local document question-answering system that processes PDF documents and allows users to ask questions about their content.

Instead of relying only on an AI model's general knowledge, RAGdocAI retrieves relevant information from documents and uses that information to generate context-based answers.

The main goal of this project is to understand and implement the complete RAG pipeline from scratch using Python and local AI models, without depending on paid APIs.

## Main Features

- [x] Load and read PDF documents.
- [x] Support multiple PDF documents.
- [x] Extract text from PDF files page by page.
- [x] Sentence-aware text chunking with controlled overlap.
- [x] Prevent broken words during chunking.
- [x] Preserve document source and page metadata.
- [x] Generate unique document-specific chunk IDs.
- [x] Generate numerical embeddings using Ollama.
- [x] Store embeddings and metadata in ChromaDB.
- [x] Retrieve relevant information using semantic similarity search.
- [x] Implement BM25 keyword search.
- [x] Combine semantic and keyword search using Reciprocal Rank Fusion (RRF).
- [x] Implement Hybrid Search.
- [x] Implement query rewriting using a local LLM.
- [x] Implement FlashRank-based reranking.
- [x] Implement similarity threshold filtering.
- [x] Integrate Hybrid Search into the main `ask_question()` function.
- [x] Return retrieved text with source and page information.
- [x] Generate answers using a locally running LLM.
- [x] Answer questions using retrieved document context.
- [x] Handle repeated PDF ingestion without creating duplicate records.
- [x] Update existing document chunks while preserving other documents.
- [x] Handle empty document collections during retrieval.
- [x] Handle empty user input.
- [x] Avoid generating answers when no documents are available.
- [x] Organize document processing into reusable functions.
- [x] Implement reusable embedding, storage, retrieval and answer-generation functions.
- [x] Connect the complete workflow through a single `ask_question()` function.
- [x] Implement retrieval evaluation using Precision@K and Recall@K.
- [x] Organize automated tests using pytest.
- [x] Verify the complete pipeline with 27 passing test cases.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Run local AI models |
| Llama 3.2 (3B) | Local language model for answer generation and query rewriting |
| Nomic Embed Text | Generate text embeddings |
| ChromaDB | Local vector database |
| PyMuPDF | Extract text from PDF documents |
| rank-bm25 | Keyword-based document retrieval |
| FlashRank | Rerank retrieved document chunks |
| pytest | Automated testing |
| Streamlit | Planned user interface |

## Project Architecture

The RAG pipeline currently implemented:

1. **Document Loading:** Read PDF files and extract text page by page using PyMuPDF.
2. **Text Chunking:** Divide extracted text into smaller pieces using sentence-aware chunking with controlled overlap.
3. **Metadata Preservation:** Attach document source, page number and unique document ID to every chunk.
4. **Embeddings:** Convert text chunks into numerical vectors using Nomic Embed Text.
5. **Vector Storage:** Store embeddings, document chunks and metadata in ChromaDB.
6. **Semantic Retrieval:** Find relevant chunks using embedding similarity.
7. **Keyword Retrieval:** Find relevant chunks using BM25 keyword search.
8. **Query Rewriting:** Expand or reformulate user questions to improve retrieval.
9. **Hybrid Retrieval:** Combine semantic and keyword search rankings using Reciprocal Rank Fusion (RRF).
10. **Reranking:** Reorder retrieved chunks using FlashRank based on their relevance to the question.
11. **Similarity Filtering:** Filter low-relevance results using a configurable score threshold.
12. **Generation:** Pass retrieved context to a local LLM using Ollama.
13. **Response:** Generate context-based answers with source and page references.

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
│   ├── text_splitter.py
│   ├── embed_chunks.py
│   ├── store_embeddings.py
│   ├── retrieve_data.py
│   ├── retrieve_chunks.py
│   ├── rag_answer.py
│   ├── rag_pipeline.py
│   ├── keyword_search.py
│   ├── hybrid_search.py
│   ├── query_rewriter.py
│   ├── reranker.py
│   └── evaluation.py
│
├── tests/
│   ├── conftest.py
│   ├── test_chromadb.py
│   ├── test_embeddings.py
│   ├── test_evaluation.py
│   ├── test_hybrid_search.py
│   ├── test_keyword_search.py
│   ├── test_loader.py
│   ├── test_pipeline.py
│   ├── test_query_rewriter.py
│   ├── test_reranker.py
│   └── test_splitter.py
│
├── .gitignore
├── .gitattributes
├── requirements.txt
└── README.md
```

**Note:**
- `data/chroma_db/` contains the locally stored ChromaDB database and is not intended to be committed to GitHub.
- The private `PROJECT_CONTEXT.md` file is excluded from GitHub.
- The `.venv/` directory and pytest cache are local development files.

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

Model downloads are required only if the models are not already available locally.

### 6. Add PDF Documents

Place your PDF files inside the `documents/` directory.

The project supports multiple PDF documents.

### 7. Ingest PDF Documents

From the project root:

```bash
python src/store_embeddings.py
```

This processes PDF files inside the `documents/` directory and stores their embeddings and metadata in ChromaDB.

### 8. Ask Questions Using the RAG Pipeline

The main pipeline is available through the reusable `ask_question()` function in `src/rag_pipeline.py`.

The module can be imported into another Python script and used to ask questions:

```python
import sys

sys.path.insert(0, "src")

from rag_pipeline import ask_question

answer = ask_question(
    "What is Python?",
    n_results=2
)

print(answer)
```

This retrieves relevant document chunks using the implemented retrieval pipeline and generates an answer using the local LLM.

**Note:** `rag_pipeline.py` currently provides reusable functions; it does not yet have a standalone interactive command-line interface.

### 9. Run Automated Tests

Run all tests from the project root:

```bash
python -m pytest tests/ -v
```

## Testing Results

The project currently contains 10 pytest test files covering the main components of the RAG pipeline.

**Latest test results:**

- Total test files: 10
- Total test cases: 27
- Passed: 27
- Failed: 0
- Execution time: 8.60 seconds

All 27 tests passed successfully in the latest complete test run.

Test coverage includes:

- PDF loading and page extraction.
- Text chunking.
- Embedding generation.
- ChromaDB connection and collection handling.
- BM25 keyword search.
- FlashRank reranking.
- Query rewriting.
- Hybrid Search.
- Precision@K and Recall@K evaluation.
- Complete RAG pipeline and empty collection handling.

**Note:** Some integration tests require Ollama and the locally available AI models. ChromaDB currently produces a dependency deprecation warning during testing; it does not cause test failures.

## Project Status

**Currently in Development**

### Completed

- [x] Project environment setup.
- [x] Python virtual environment configuration.
- [x] Required Python libraries installed.
- [x] Ollama installation and local model verification.
- [x] PDF text extraction using PyMuPDF.
- [x] Page-wise PDF text extraction.
- [x] Sentence-aware text chunking.
- [x] Controlled overlap between chunks.
- [x] Prevent broken words during chunking.
- [x] Preserve page metadata in text chunks.
- [x] Generate text embeddings using Ollama.
- [x] Verify embedding dimensions.
- [x] Integrate ChromaDB.
- [x] Store document chunks and embeddings in ChromaDB.
- [x] Store source, page and document ID metadata.
- [x] Synchronize updated chunks with ChromaDB.
- [x] Generate unique document-specific chunk IDs.
- [x] Implement semantic document retrieval.
- [x] Connect the local LLM with retrieved context.
- [x] Generate context-based answers using Llama 3.2.
- [x] Handle insufficient information using grounded answering.
- [x] Handle empty user input.
- [x] Handle empty document collections during retrieval.
- [x] Implement reusable PDF processing, embedding, storage and retrieval functions.
- [x] Connect the complete workflow through `ask_question()`.
- [x] Support multiple PDF documents.
- [x] Verify repeated ingestion without duplicate records.
- [x] Implement BM25 keyword search.
- [x] Implement Hybrid Search using semantic and keyword retrieval.
- [x] Combine search rankings using Reciprocal Rank Fusion.
- [x] Implement query rewriting.
- [x] Implement FlashRank reranking.
- [x] Implement similarity threshold filtering.
- [x] Implement retrieval evaluation using Precision@K and Recall@K.
- [x] Add automated pytest tests.
- [x] Verify all 27 tests successfully.

### In Progress

- [ ] Organize and clean up the project for the next development stage.
- [ ] Review retrieval quality and improve evaluation coverage.

### Upcoming

- [ ] Develop a Streamlit user interface.
- [ ] Support multiple document formats.
- [ ] Allow document uploads through the interface.
- [ ] Display source-based answers with document references.
- [ ] Add document management.
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
- Further improvements to retrieval quality.
- More comprehensive retrieval evaluation.
- Streamlit-based user interface.
- Document management and chat history.

## Learning Approach

This project is being developed step by step, starting with the fundamentals of RAG before moving towards advanced techniques.

The focus is on understanding the internal working of each component rather than simply using ready-made frameworks.

---

**Project Name:** RAGdocAI  
**Language:** Python  
**Approach:** Local-first RAG  
**Status:** In Development

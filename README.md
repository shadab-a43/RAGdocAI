# RAGdocAI

A beginner-friendly, local-first AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

## About the Project

RAGdocAI is a local document question-answering application that processes PDF documents and allows users to ask questions about their content through a web-based interface.

Instead of relying only on an AI model's general knowledge, RAGdocAI retrieves relevant information from uploaded documents and uses that context to generate answers.

The project combines a complete RAG pipeline with a locally hosted web application. It uses Python, FastAPI, Ollama and ChromaDB without requiring paid AI APIs.

The main goal is to understand and implement the complete RAG pipeline while learning how to connect a Python backend with a modern frontend.

## Main Features

### Document Processing and Retrieval

- [x] Load and read PDF documents.
- [x] Support multiple PDF documents.
- [x] Extract PDF text page by page using PyMuPDF.
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
- [x] Return retrieved text with source and page information.
- [x] Generate answers using a locally running LLM.
- [x] Handle insufficient information and empty document collections.
- [x] Handle repeated PDF ingestion without creating duplicate records.
- [x] Update existing document chunks while preserving other documents.
- [x] Implement retrieval evaluation using Precision@K and Recall@K.
- [x] Organize automated tests using pytest.
- [x] Verify the complete pipeline with 27 passing test cases.

### Web Application

- [x] Build a FastAPI backend.
- [x] Create a frontend using HTML, CSS and JavaScript.
- [x] Implement PDF uploads through the web interface.
- [x] Support uploading multiple PDF files.
- [x] Automatically process uploaded PDFs and store their chunks.
- [x] Connect the frontend with the backend using API endpoints.
- [x] Implement an interactive document question-answering interface.
- [x] Display AI-generated answers.
- [x] Display document source and page references.
- [x] Add clickable question suggestions.
- [x] Implement Light and Dark themes.
- [x] Add rounded cards, gradients and responsive styling.
- [x] Automatically scroll to the latest chat message.
- [x] Keep the question input area at the bottom of the chat workspace.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend web framework |
| Uvicorn | ASGI application server |
| HTML | Frontend structure |
| CSS | Frontend styling and themes |
| JavaScript | Frontend interactions and API communication |
| Ollama | Run local AI models |
| Llama 3.2 (3B) | Answer generation and query rewriting |
| Nomic Embed Text | Generate text embeddings |
| ChromaDB | Local vector database |
| PyMuPDF | Extract text from PDF documents |
| rank-bm25 | Keyword-based document retrieval |
| FlashRank | Rerank retrieved document chunks |
| python-multipart | Handle PDF file uploads |
| pytest | Automated testing |

## Project Architecture

### RAG Pipeline

1. **Document Loading:** Read PDF files and extract text page by page using PyMuPDF.
2. **Text Chunking:** Divide extracted text into smaller pieces using sentence-aware chunking with controlled overlap.
3. **Metadata Preservation:** Attach document source, page number and unique document ID to every chunk.
4. **Embeddings:** Convert text chunks into numerical vectors using Nomic Embed Text.
5. **Vector Storage:** Store embeddings, document chunks and metadata in ChromaDB.
6. **Semantic Retrieval:** Find relevant chunks using embedding similarity.
7. **Keyword Retrieval:** Find relevant chunks using BM25 keyword search.
8. **Query Rewriting:** Reformulate user questions to improve retrieval.
9. **Hybrid Retrieval:** Combine semantic and keyword search rankings using Reciprocal Rank Fusion (RRF).
10. **Reranking:** Reorder retrieved chunks using FlashRank based on their relevance to the question.
11. **Similarity Filtering:** Filter low-relevance results using a configurable score threshold.
12. **Generation:** Pass retrieved context to a local LLM using Ollama.
13. **Response:** Generate context-based answers with source and page references.

### Web Application Architecture

The web application connects the frontend to the RAG pipeline through FastAPI.

1. **Frontend:** HTML provides the application structure.
2. **Styling:** CSS provides the layout, responsive design, gradients and theme support.
3. **Frontend Logic:** JavaScript handles PDF uploads, chat interactions and API requests.
4. **Backend:** FastAPI provides endpoints for the homepage, health check, PDF uploads and questions.
5. **Document Upload:** Uploaded PDFs are saved in the local `documents/` directory and processed through the RAG pipeline.
6. **Question Processing:** Questions are sent to the backend, which calls the reusable `ask_question()` function.
7. **AI Response:** The backend returns the generated answer to the frontend, including source information.

## Project Structure

```text
RAGdocAI/
│
├── app.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
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
- `PROJECT_CONTEXT.md` is a private project context file and is excluded from GitHub.
- `.venv/` and pytest cache are local development files.
- Uploaded PDFs are stored locally in `documents/`.

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

Make sure Ollama is running before starting the application.

### 6. Start the Web Application

From the project root, run:

```bash
python -m uvicorn app:app --reload
```

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

The application runs locally on your computer.

### 7. Upload PDF Documents

1. Open RAGdocAI in your browser.
2. Click **Add PDF files**.
3. Select one or multiple PDF documents.
4. Wait for document processing to complete.
5. The application displays the processing status and number of stored chunks.

Uploaded documents are saved in the local `documents/` directory.

### 8. Ask Questions

After uploading documents, enter a question in the chat input.

The application retrieves relevant information from the documents and generates an answer using the local AI model.

Answers include available document source and page references.

### 9. Run Automated Tests

Run all tests from the project root:

```bash
python -m pytest tests/ -v
```

## API Endpoints

The FastAPI backend currently provides the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve the web application |
| GET | `/health` | Check application status |
| POST | `/upload` | Upload and process a PDF |
| POST | `/ask` | Ask a question about documents |

## Testing Results

The project currently contains 10 pytest test files covering the main components of the RAG pipeline.

**Latest complete test results:**

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
- [x] Ollama installation and local model verification.
- [x] PDF text extraction using PyMuPDF.
- [x] Sentence-aware text chunking.
- [x] Controlled overlap and word-safe chunking.
- [x] Page and document metadata preservation.
- [x] Embedding generation using Ollama.
- [x] ChromaDB integration and storage.
- [x] Semantic document retrieval.
- [x] BM25 keyword search.
- [x] Hybrid Search using Reciprocal Rank Fusion.
- [x] Query rewriting.
- [x] FlashRank reranking.
- [x] Similarity threshold filtering.
- [x] Context-based answer generation using Llama 3.2.
- [x] Source-based answers.
- [x] Multiple PDF document support.
- [x] Duplicate ingestion handling.
- [x] Reusable RAG pipeline through `ask_question()`.
- [x] Retrieval evaluation using Precision@K and Recall@K.
- [x] Automated pytest testing with 27 passing tests.
- [x] FastAPI backend integration.
- [x] HTML, CSS and JavaScript frontend.
- [x] PDF upload through the web interface.
- [x] Interactive document chat.
- [x] Source and page reference display.
- [x] Light and Dark theme support.
- [x] Responsive frontend styling.
- [x] Automatic chat scrolling and bottom-positioned question input.

### Upcoming

- [ ] Improve document management.
- [ ] Add chat history.
- [ ] Support additional document formats.
- [ ] Improve retrieval quality and evaluation coverage.
- [ ] Further improve application performance and user experience.

## Project Goals

- Understand how Retrieval-Augmented Generation works internally.
- Learn document processing and text chunking.
- Understand embeddings and vector databases.
- Build a complete RAG pipeline from scratch.
- Integrate a local AI model with a web application.
- Use locally running AI models without paid API dependencies.
- Explore advanced RAG techniques.
- Build a practical portfolio project.

## Privacy

RAGdocAI is designed around local processing using Ollama and locally stored project data.

No paid API keys are required for the core functionality.

Documents, embeddings and the vector database are stored locally on the computer. Internet access may be needed initially to download Python packages and AI models.

## Future Improvements

- Support for PDF, TXT and DOCX documents.
- Improved chunking strategies.
- Further improvements to retrieval quality.
- More comprehensive retrieval evaluation.
- Document management.
- Chat history.
- Additional frontend improvements.

## Learning Approach

This project is being developed step by step, starting with the fundamentals of RAG before moving towards advanced techniques and web application development.

The focus is on understanding the internal working of each component rather than simply using ready-made frameworks.

---

**Project Name:** RAGdocAI  
**Language:** Python, JavaScript  
**Backend:** FastAPI  
**Frontend:** HTML, CSS, JavaScript  
**Approach:** Local-first RAG  
**Status:** In Development

import hashlib
import re
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.rag_pipeline import (
    ingest_pdf,
    ask_question,
    find_duplicate_pdf,
    get_uploaded_documents,
    delete_document_chunks
)


# ========================================
# 1. PROJECT CONFIGURATION
# ========================================

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = (BASE_DIR / "documents").resolve()
DOCUMENTS_DIR.mkdir(exist_ok=True)


# ========================================
# 2. FASTAPI APPLICATION
# ========================================

app = FastAPI(
    title="RAGdocAI",
    description="Intelligent Document Retrieval & AI-Powered Answers",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# ========================================
# 3. HOMEPAGE
# ========================================

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")


# ========================================
# 4. HEALTH CHECK
# ========================================

@app.get("/health")
def health_check():
    return {
        "status": "running",
        "application": "RAGdocAI"
    }


# ========================================
# 5. PDF UPLOAD
# ========================================

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF is empty."
        )

    file_hash = hashlib.sha256(content).hexdigest()

    # Find the existing PDF with identical content
    existing_filename = find_duplicate_pdf(file_hash)

    if existing_filename:
        return {
            "uploaded": False,
            "duplicate": True,
            "message": "This PDF is already uploaded. Duplicate skipped.",
            "filename": existing_filename
        }

    original_filename = Path(file.filename).name

    file_path = DOCUMENTS_DIR / original_filename

    # Avoid overwriting a different PDF
    if file_path.exists():

        file_stem = Path(original_filename).stem
        file_extension = Path(original_filename).suffix

        counter = 1

        while file_path.exists():

            unique_filename = (
                f"{file_stem}_{file_hash[:8]}_{counter}"
                f"{file_extension}"
            )

            file_path = DOCUMENTS_DIR / unique_filename
            counter += 1

    try:

        file_path.write_bytes(content)

        total_chunks = ingest_pdf(str(file_path))

        return {
            "uploaded": True,
            "duplicate": False,
            "message": "PDF uploaded and processed successfully.",
            "filename": file_path.name,
            "total_chunks": total_chunks
        }

    except Exception:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="PDF processing failed. Please check the PDF and try again."
        )


# ========================================
# 6. GET UPLOADED DOCUMENTS
# ========================================

@app.get("/documents")
def list_documents():

    try:

        documents = get_uploaded_documents()

        return {
            "total_documents": len(documents),
            "documents": documents
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve uploaded documents."
        )


# ========================================
# 7. DELETE A DOCUMENT
# ========================================

@app.delete("/documents/{document_id}")
def delete_document(document_id: str):

    # Validate document ID format
    if not re.fullmatch(r"[0-9a-f]{16}", document_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID."
        )

    try:

        # Find the selected document
        documents = get_uploaded_documents()

        selected_document = next(
            (
                document
                for document in documents
                if document["document_id"] == document_id
            ),
            None
        )

        if selected_document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        filename = selected_document["filename"]

        # Allow only a plain PDF filename
        if Path(filename).name != filename or not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Invalid document filename."
            )

        file_path = (DOCUMENTS_DIR / filename).resolve()

        # Confirm that the PDF belongs to documents folder
        if file_path.parent != DOCUMENTS_DIR:
            raise HTTPException(
                status_code=400,
                detail="Invalid document location."
            )

        # Delete only this document's ChromaDB chunks
        deleted_chunks = delete_document_chunks(document_id)

        # Delete the physical PDF if it exists
        if file_path.exists():
            file_path.unlink()

        return {
            "deleted": True,
            "filename": filename,
            "deleted_chunks": deleted_chunks,
            "message": "Document and its stored chunks deleted successfully."
        }

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Document deletion failed. Please try again."
        )


# ========================================
# 8. QUESTION REQUEST MODEL
# ========================================

class QuestionRequest(BaseModel):
    question: str


# ========================================
# 9. ASK QUESTION
# ========================================

@app.post("/ask")
def ask_document(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        answer = ask_question(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Question processing failed. Please try again."
        )

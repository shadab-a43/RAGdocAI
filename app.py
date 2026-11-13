
import hashlib
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.rag_pipeline import (
    ingest_pdf,
    ask_question,
    is_duplicate_pdf
)


# ========================================
# 1. PROJECT CONFIGURATION
# ========================================

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = BASE_DIR / "documents"
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

    # Step 1: Generate content hash
    file_hash = hashlib.sha256(content).hexdigest()

    # Step 2: Check for duplicate PDF
    if is_duplicate_pdf(file_hash):

        return {
            "uploaded": False,
            "duplicate": True,
            "message": "This PDF is already uploaded. Duplicate skipped.",
            "filename": Path(file.filename).name
        }

    # Step 3: Create a safe filename
    original_filename = Path(file.filename).name

    file_path = DOCUMENTS_DIR / original_filename

    # Avoid overwriting a different PDF with the same filename
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

        # Step 4: Save the new PDF
        file_path.write_bytes(content)

        # Step 5: Process and store PDF chunks
        total_chunks = ingest_pdf(str(file_path))

        return {
            "uploaded": True,
            "duplicate": False,
            "message": "PDF uploaded and processed successfully.",
            "filename": file_path.name,
            "total_chunks": total_chunks
        }

    except Exception:
        # Remove the saved file if processing fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="PDF processing failed. Please check the PDF and try again."
        )


# ========================================
# 6. QUESTION REQUEST MODEL
# ========================================

class QuestionRequest(BaseModel):
    question: str


# ========================================
# 7. ASK QUESTION
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

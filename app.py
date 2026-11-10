
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.rag_pipeline import ingest_pdf, ask_question


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Documents directory
DOCUMENTS_DIR = BASE_DIR / "documents"
DOCUMENTS_DIR.mkdir(exist_ok=True)


# Create FastAPI application
app = FastAPI(
    title="RAGdocAI",
    description="Intelligent Document Retrieval & AI-Powered Answers",
    version="1.0.0"
)


# Connect CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# Homepage
@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "running",
        "application": "RAGdocAI"
    }


# PDF upload endpoint
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = DOCUMENTS_DIR / Path(file.filename).name

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )

        with open(file_path, "wb") as pdf_file:
            pdf_file.write(content)

        total_chunks = ingest_pdf(str(file_path))

        return {
            "message": "PDF uploaded and processed successfully.",
            "filename": file.filename,
            "total_chunks": total_chunks
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(error)}"
        )


# Question request model
class QuestionRequest(BaseModel):
    question: str


# Ask question endpoint
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

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(error)}"
        )

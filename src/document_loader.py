
import pymupdf
from pathlib import Path


def load_pdf_pages(file_path):
    """Extract text from a PDF page by page."""

    pages = []

    # Step 1: Open PDF
    document = pymupdf.open(file_path)

    # Step 2: Extract text from each page
    for page_number, page in enumerate(document, start=1):

        page_data = {
            "source": Path(file_path).name,
            "page": page_number,
            "text": page.get_text()
        }

        pages.append(page_data)

    # Step 3: Close PDF
    document.close()

    return pages


def load_pdf(file_path):
    """Extract all text from a PDF file."""

    pages = load_pdf_pages(file_path)

    # Combine page text into one string
    text = "\n".join(
        page["text"] for page in pages
    )

    return text

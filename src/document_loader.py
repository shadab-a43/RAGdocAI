
import pymupdf


def load_pdf(file_path):
    """Extract text from a PDF file."""

    text = ""

    document = pymupdf.open(file_path)

    for page in document:
        text += page.get_text() + "\n"

    document.close()

    return text

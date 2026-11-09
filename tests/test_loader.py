
from document_loader import load_pdf, load_pdf_pages


def test_load_pdf():
    text = load_pdf("documents/sample.pdf")

    assert isinstance(text, str)
    assert len(text) > 0


def test_load_pdf_pages():
    pages = load_pdf_pages("documents/sample.pdf")

    assert len(pages) > 0

    for page in pages:
        assert "source" in page
        assert "page" in page
        assert "text" in page
        assert len(page["text"]) > 0

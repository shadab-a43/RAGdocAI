
from text_splitter import split_text, split_pages


def test_split_text():
    text = "Python is a programming language. " * 30

    chunks = split_text(
        text,
        chunk_size=20,
        overlap=5
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert isinstance(chunk, str)
        assert len(chunk.split()) <= 20


def test_split_pages():
    pages = [
        {
            "source": "sample.pdf",
            "page": 1,
            "text": "Python is a programming language. " * 30
        }
    ]

    chunks = split_pages(
        pages,
        chunk_size=20,
        overlap=5
    )

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk["source"] == "sample.pdf"
        assert chunk["page"] == 1
        assert len(chunk["text"]) > 0

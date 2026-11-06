
import re


def split_text(text, chunk_size=200, overlap=30):
    """Split text into sentence-aware chunks with word-safe overlap."""

    # Step 1: Clean PDF whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Step 2: Split text into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Step 3: Break unusually long sentences at word boundaries
    units = []

    for sentence in sentences:
        words = sentence.split()
        part = ""

        for word in words:
            candidate = f"{part} {word}".strip()

            if len(candidate) > chunk_size and part:
                units.append(part)
                part = word
            else:
                part = candidate

        if part:
            units.append(part)

    # Step 4: Create chunks with overlap
    chunks = []
    current_chunk = ""

    for unit in units:

        candidate = f"{current_chunk} {unit}".strip()

        if not current_chunk or len(candidate) <= chunk_size:
            current_chunk = candidate

        else:
            chunks.append(current_chunk)

            # Keep previous words as overlap
            capacity = chunk_size - len(unit) - 1
            overlap_limit = min(overlap, capacity)

            previous_words = current_chunk.split()
            overlap_words = []

            for word in reversed(previous_words):
                test = " ".join([word] + overlap_words)

                if len(test) <= overlap_limit:
                    overlap_words.insert(0, word)
                else:
                    break

            overlap_text = " ".join(overlap_words)
            current_chunk = f"{overlap_text} {unit}".strip()

    # Step 5: Save remaining chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def split_pages(pages, chunk_size=200, overlap=30):
    """Split PDF pages into chunks while preserving source metadata."""

    all_chunks = []

    # Process each page separately
    for page in pages:

        # Split page text using existing chunking function
        chunks = split_text(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        # Attach source and page information to every chunk
        for chunk in chunks:

            chunk_data = {
                "text": chunk,
                "source": page["source"],
                "page": page["page"]
            }

            all_chunks.append(chunk_data)

    return all_chunks


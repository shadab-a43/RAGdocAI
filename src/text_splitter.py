
import re


def split_text(text, chunk_size=200, overlap=30):
    """Split text into chunks without breaking words."""

    # Step 1: Clean PDF whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Step 2: Split text into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""

    # Step 3: Process each sentence
    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # Step 4: Handle sentences longer than chunk_size
        if len(sentence) > chunk_size:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            words = sentence.split()
            part = ""

            for word in words:

                if part and len(part) + len(word) + 1 > chunk_size:
                    chunks.append(part)
                    part = word
                else:
                    part = f"{part} {word}".strip()

            if part:
                current_chunk = part

            continue

        # Step 5: Add sentence to current chunk
        if current_chunk and len(current_chunk) + len(sentence) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk = f"{current_chunk} {sentence}".strip()

    # Step 6: Save the remaining chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

import re


def clean_text(text):
    """
    Clean extracted PDF text.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=400, overlap=80):
    """
    Split text into overlapping word-based chunks.
    """

    text = clean_text(text)

    words = text.split()

    # Ignore extremely small pieces
    if len(words) < 30:
        return []

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if len(chunk.split()) >= 30:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
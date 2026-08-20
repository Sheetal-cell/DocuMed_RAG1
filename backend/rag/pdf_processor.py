from pypdf import PdfReader


def extract_pdf_chunks(
    pdf_path,
    source_name,
    chunk_size=1000,
    chunk_overlap=200
):
    """
    Extract text from a PDF page-by-page and split it into chunks.

    Each chunk keeps its original PDF page number so that
    DocuMed can show accurate sources to the user.
    """

    reader = PdfReader(pdf_path)

    chunks = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        # Clean excessive whitespace
        text = " ".join(text.split())

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "source": source_name,
                    "page": page_number
                })

            # Move forward while keeping overlap
            start += chunk_size - chunk_overlap

    return chunks
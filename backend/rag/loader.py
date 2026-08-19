import pymupdf
from pathlib import Path


def load_pdf(pdf_path: str):
    """
    Extract text from a PDF.

    Returns a list of pages with their page numbers.
    """

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text.strip()
            })

    document.close()

    return pages
from rag.loader import load_pdf
from rag.chunker import chunk_text
from rag.embeddings import embed_texts
from rag.vectorstore import add_documents


PDF_PATH = "data/documents/heart.pdf"


# --------------------------------
# 1. Load PDF
# --------------------------------

pages = load_pdf(PDF_PATH)

print("Pages loaded:", len(pages))


# --------------------------------
# 2. Create chunks
# --------------------------------

all_chunks = []

for page in pages:

    chunks = chunk_text(
        page["text"],
        chunk_size=400,
        overlap=80
    )

    for chunk in chunks:

        all_chunks.append({
            "source": "heart.pdf",
            "page": page["page"],
            "text": chunk
        })


print("Total chunks:", len(all_chunks))


# --------------------------------
# 3. Create embeddings
# --------------------------------

texts = [
    chunk["text"]
    for chunk in all_chunks
]

embeddings = embed_texts(texts)

print("Embeddings created:", len(embeddings))


# --------------------------------
# 4. Store in ChromaDB
# --------------------------------

add_documents(
    all_chunks,
    embeddings
)

print("Documents successfully added to ChromaDB!")
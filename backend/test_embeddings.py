from rag.loader import load_pdf
from rag.chunker import chunk_text
from rag.embeddings import embed_texts


PDF_PATH = "data/documents/heart.pdf"

pages = load_pdf(PDF_PATH)

all_chunks = []

for page in pages:

    chunks = chunk_text(
        page["text"],
        chunk_size=500,
        overlap=100
    )

    for chunk in chunks:

        all_chunks.append({
            "source": "heart.pdf",
            "page": page["page"],
            "text": chunk
        })


texts = [
    chunk["text"]
    for chunk in all_chunks
]

embeddings = embed_texts(texts)

print("Chunks:", len(texts))
print("Embeddings:", len(embeddings))

print("Embedding dimension:", len(embeddings[0]))

print("\nFirst embedding:")
print(embeddings[0][:10])
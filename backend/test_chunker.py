from rag.loader import load_pdf
from rag.chunker import chunk_text


pages = load_pdf("data/documents/heart.pdf")

all_chunks = []

for page in pages:

    chunks = chunk_text(
        page["text"],
        chunk_size=500,
        overlap=100
    )

    for chunk in chunks:
        all_chunks.append({
            "page": page["page"],
            "text": chunk
        })


print("Total chunks:", len(all_chunks))

for i, chunk in enumerate(all_chunks[:3]):

    print("\n--------------------")
    print("Chunk:", i)
    print("Page:", chunk["page"])
    print(chunk["text"][:500])
import uuid

import chromadb


client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="documed_documents"
)


def add_documents(chunks, embeddings):

    ids = [
        f"chunk_{uuid.uuid4().hex}"
        for _ in chunks
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def search(query_embedding, top_k=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
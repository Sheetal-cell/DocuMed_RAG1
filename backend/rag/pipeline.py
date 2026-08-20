from backend.rag.embeddings import embed_query
from backend.rag.vectorstore import search
from backend.rag.prompt import build_prompt


def retrieve_context(question, top_k=3):

    # Convert question into embedding
    query_embedding = embed_query(question)

    # Search vector database
    results = search(
        query_embedding,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    distances = results["distances"][0]

    return documents, metadata, distances


def create_rag_prompt(question, top_k=3):

    documents, metadata, distances = retrieve_context(
        question,
        top_k=top_k
    )

    prompt = build_prompt(
        question,
        documents,
        metadata
    )

    return {
        "prompt": prompt,
        "documents": documents,
        "metadata": metadata,
        "distances": distances
    }


def create_sources(metadata, distances, documents):

    sources = []

    for meta, distance, document in zip(
        metadata,
        distances,
        documents
    ):

        similarity = 1 - float(distance)

        sources.append({
            "source": meta["source"],
            "page": meta["page"],
            "similarity": round(similarity, 4),
            "chunk": document
        })

    return sources
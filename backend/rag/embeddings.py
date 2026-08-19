from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_embedding_model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts):
    """
    Convert a list of texts into embedding vectors.
    """

    embeddings = _embedding_model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def embed_query(query):
    """
    Convert a single query into an embedding.
    """

    embedding = _embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()
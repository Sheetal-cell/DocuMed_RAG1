from rag.embeddings import embed_query
from rag.vectorstore import search


question = """
What are the major recommendations for cardiovascular
disease management in primary health care?
"""


# --------------------------------
# 1. Convert question to embedding
# --------------------------------

query_embedding = embed_query(question)


# --------------------------------
# 2. Search ChromaDB
# --------------------------------

results = search(
    query_embedding,
    top_k=3
)


# --------------------------------
# 3. Display results
# --------------------------------

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for i in range(len(documents)):

    print("\n========================================")
    print(f"RESULT {i + 1}")
    print("========================================")

    print("Source:", metadatas[i]["source"])
    print("Page:", metadatas[i]["page"])
    print("Distance:", distances[i])

    print("\nTEXT:")
    print(documents[i])
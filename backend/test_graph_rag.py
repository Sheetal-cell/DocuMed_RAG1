from backend.graph_rag.graph_store import (
    get_graph
)

from backend.graph_rag.graph_builder import (
    build_graph
)

from backend.graph_rag.graph_retriever import (
    retrieve_graph_context
)


chunks = [
    {
        "text": """
        Hypertension increases the risk of stroke.
        Smoking increases the risk of hypertension.
        """
    }
]


print("Building knowledge graph...")

count = build_graph(
    chunks
)

print(
    "Relationships created:",
    count
)


print("\nNodes:")

graph = get_graph()

for node in graph.nodes:

    print("-", node)


print("\nRelationships:")

for source, target, data in graph.edges(
    data=True
):

    print(
        source,
        "--",
        data["relationship"],
        "-->",
        target
    )


print("\nGraph retrieval:")

question = "What increases the risk of hypertension?"

results = retrieve_graph_context(
    question
)

for result in results:

    print("-", result)
from backend.graph_rag.graph_store import (
    get_related_entities,
    get_graph
)


def retrieve_graph_context(question):

    graph = get_graph()

    question_words = set(
        question.lower().split()
    )

    matched_entities = []

    for node in graph.nodes:

        node_words = set(
            str(node).lower().split()
        )

        if question_words.intersection(node_words):

            matched_entities.append(node)

    context = []

    for entity in matched_entities:

        related = get_related_entities(
            entity
        )

        for item in related:

            context.append(
                f"{entity} "
                f"{item['relationship']} "
                f"{item['entity']}"
            )

    return context
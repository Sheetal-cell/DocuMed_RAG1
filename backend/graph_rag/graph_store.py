import networkx as nx


graph = nx.MultiDiGraph()


def add_relationship(
    source_entity,
    relationship,
    target_entity,
    source_file=None,
    page=None
):
    """
    Add a relationship to the knowledge graph.
    """

    graph.add_node(source_entity)
    graph.add_node(target_entity)

    graph.add_edge(
        source_entity,
        target_entity,
        relationship=relationship,
        source_file=source_file,
        page=page
    )


def get_related_entities(entity):

    if entity not in graph:
        return []

    results = []

    for _, target, data in graph.out_edges(
        entity,
        data=True
    ):

        results.append({
            "entity": target,
            "relationship": data["relationship"],
            "source": data.get("source_file"),
            "page": data.get("page")
        })

    return results


def get_graph():

    return graph
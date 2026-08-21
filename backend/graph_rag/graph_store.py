import networkx as nx

# Knowledge graph
graph = nx.MultiDiGraph()


def add_relationship(source, relationship, target):
    """
    Add a relationship between two entities.
    """

    graph.add_node(source)
    graph.add_node(target)

    graph.add_edge(
        source,
        target,
        relationship=relationship
    )


def get_related_entities(entity):
    """
    Return entities directly connected to the given entity.
    """

    if entity not in graph:
        return []

    results = []

    for _, target, data in graph.out_edges(
        entity,
        data=True
    ):
        results.append({
            "entity": target,
            "relationship": data["relationship"]
        })

    return results


def get_graph():
    """
    Return the complete knowledge graph.
    """

    return graph
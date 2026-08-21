import re

from backend.graph_rag.graph_store import add_relationship


def extract_relationships(text):
    """
    Extract simple relationships from text.
    """

    relationships = []

    sentences = re.split(
        r"[.!?]",
        text
    )

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        pattern = re.search(
            r"(.+?)\s+(increases the risk of|causes|leads to|associated with)\s+(.+)",
            sentence,
            re.IGNORECASE
        )

        if pattern:

            source = pattern.group(1).strip()
            relationship = pattern.group(2).strip()
            target = pattern.group(3).strip()

            relationships.append({
                "source": source,
                "relationship": relationship,
                "target": target
            })

    return relationships


def build_graph(chunks):

    total_relationships = 0

    for chunk in chunks:

        relationships = extract_relationships(
            chunk["text"]
        )

        for item in relationships:

            add_relationship(
                item["source"],
                item["relationship"],
                item["target"],
                source_file=chunk.get("source"),
                page=chunk.get("page")
            )

            total_relationships += 1

    return total_relationships
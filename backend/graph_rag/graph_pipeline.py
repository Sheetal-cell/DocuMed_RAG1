from backend.graph_rag.graph_retriever import (
    retrieve_graph_context
)

from backend.rag.llm_local_small import (
    generate_answer
)


def create_graph_prompt(question):

    context = retrieve_graph_context(
        question
    )

    if not context:

        return None

    graph_context = "\n".join(
        context
    )

    prompt = f"""
You are DocuMed, a medical document
question answering assistant.

Answer the user's question using only
the information provided in the knowledge graph.

Knowledge graph:

{graph_context}

Question:

{question}

If the graph does not contain enough
information, say that the information
is not available in the graph.

Answer clearly and concisely.
"""

    return prompt


def graph_answer(question):

    prompt = create_graph_prompt(
        question
    )

    if prompt is None:

        return {
            "answer": "No relevant information found in the knowledge graph.",
            "graph_context": []
        }

    answer = generate_answer(
        prompt
    )

    return {
        "answer": answer,
        "graph_context": prompt
    }
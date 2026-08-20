def build_prompt(question, retrieved_documents, retrieved_metadata):

    context_parts = []

    for i in range(len(retrieved_documents)):

        source = retrieved_metadata[i]["source"]
        page = retrieved_metadata[i]["page"]
        text = retrieved_documents[i]

        context_parts.append(
            f"--- DOCUMENT {i + 1} ---\n"
            f"Source: {source}\n"
            f"Page: {page}\n\n"
            f"{text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
MEDICAL DOCUMENT CONTEXT:

{context}


USER QUESTION:

{question}


INSTRUCTIONS:

Answer the user's question using ONLY the medical document
context above.

Do not use information from outside the documents.

If the answer is present in the documents:
- Answer directly.
- Keep the answer concise.
- Use the exact information supported by the documents.
- Include the relevant source and page.

Format the source citation like:

(Source: heart.pdf, Page: 8)

If the answer cannot be found in the provided documents,
respond exactly:

"I could not find this information in the provided documents."

Do not diagnose.
Do not prescribe medication.
Do not provide personalized treatment decisions.

ANSWER:
"""

    return prompt
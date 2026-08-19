def build_prompt(question, retrieved_documents, retrieved_metadata):

    context_parts = []

    for i in range(len(retrieved_documents)):

        source = retrieved_metadata[i]["source"]
        page = retrieved_metadata[i]["page"]
        text = retrieved_documents[i]

        context_parts.append(
            f"[Source: {source}, Page: {page}]\n"
            f"{text}"
        )

    context = "\n\n".join(context_parts)


    prompt = f"""
You are DocuMed, a medical information assistant.

Your job is to answer questions using ONLY the provided
medical context.

Rules:

1. Do not invent medical facts.
2. If the answer is not present in the context, say:
   "I could not find this information in the provided documents."
3. Give a clear and concise answer.
4. Mention the source document and page when possible.
5. Do not diagnose the user.
6. Do not prescribe medication.
7. For emergencies, advise the user to seek immediate
   professional medical care.

Medical Context:

{context}

User Question:

{question}

Answer:
"""

    return prompt
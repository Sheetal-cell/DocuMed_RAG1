from rag.llm_local_small import generate_answer


context = """
The HEARTS technical package provides a strategic approach
to improving cardiovascular health.

It comprises six modules and an implementation guide.

The package supports Ministries of Health to strengthen
cardiovascular disease management in primary care.
"""


question = "What is the HEARTS technical package?"


prompt = f"""
Context:

{context}

Question:

{question}

Answer using only the context.
"""


answer = generate_answer(prompt)


print()
print("========================================")
print("DOCUMED LOCAL LLM RESPONSE")
print("========================================")
print(answer)

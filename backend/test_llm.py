from backend.rag.llm_local import generate_answer


prompt = """
You are DocuMed, a medical information assistant.

Answer the question using the provided information.

Context:
Hypertension is a condition characterized by persistently
elevated blood pressure.

Question:
What is hypertension?

Answer:
"""


answer = generate_answer(prompt)

print("\n================================")
print("QWEN RESPONSE")
print("================================")
print(answer)
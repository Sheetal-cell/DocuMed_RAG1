from rag.llm import generate_answer


prompt = """
Context:

The HEARTS technical package provides a strategic approach
to improving cardiovascular health. It comprises six modules
and an implementation guide.

Question:

What is the HEARTS technical package?
"""


answer = generate_answer(prompt)


print("\n========================================")
print("LOCAL LLM ANSWER")
print("========================================")

print(answer)
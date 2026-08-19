from rag.pipeline import create_rag_prompt
from rag.llm import generate_answer


question = """
What is the HEARTS technical package and what is its purpose?
"""


# ========================================
# STEP 1 — RETRIEVE DOCUMENTS
# ========================================

result = create_rag_prompt(question)


print("\n========================================")
print("RETRIEVED SOURCES")
print("========================================")


for metadata, distance in zip(
    result["metadata"],
    result["distances"]
):

    print(
        f'{metadata["source"]} '
        f'→ Page {metadata["page"]} '
        f'→ Distance {distance:.4f}'
    )


# ========================================
# STEP 2 — SHOW PROMPT
# ========================================

print("\n========================================")
print("PROMPT SENT TO QWEN")
print("========================================")

print(result["prompt"])


# ========================================
# STEP 3 — SEND PROMPT TO QWEN
# ========================================

print("\n========================================")
print("GENERATING ANSWER...")
print("========================================")

answer = generate_answer(
    result["prompt"]
)


# ========================================
# STEP 4 — DISPLAY ANSWER
# ========================================

print("\n========================================")
print("DOCUMED ANSWER")
print("========================================")

print(answer)
from backend.rag.pipeline import create_rag_prompt, create_sources
from backend.rag.llm_local_small import generate_answer


question = """
What is the HEARTS technical package and what is its purpose?
"""


# ========================================
# STEP 1 — RETRIEVE DOCUMENTS
# ========================================

result = create_rag_prompt(
    question,
    top_k=5
)


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

print("\n========================================")
print("DOCUMED ANSWER")
print("========================================")

answer = generate_answer(
    result["prompt"]
)
sources = create_sources(
    result["metadata"],
    result["distances"]
)

print(answer)

print("\n========================================")
print("SOURCES")
print("========================================")

for source in sources:

    print(
        f'(Source: {source["source"]}, '
        f'Page: {source["page"]}, '
        f'Distance: {source["distance"]})'
    )







from rag.pipeline import create_rag_prompt


question = """
What is the HEARTS technical package and what is its purpose?
"""


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


print("\n========================================")
print("PROMPT SENT TO QWEN")
print("========================================")

print(result["prompt"])
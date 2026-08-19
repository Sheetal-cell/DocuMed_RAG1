from rag.loader import load_pdf


pdf_path = "data/documents/heart.pdf"

pages = load_pdf(pdf_path)

print("Number of pages:", len(pages))

for page in pages[:2]:
    print("\nPAGE:", page["page"])
    print(page["text"][:1000])
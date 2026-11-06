
from document_loader import load_pdf
from document_loader import load_pdf_pages

text = load_pdf("documents/sample.pdf")

print(text)

# Test page-wise PDF loading
pages = load_pdf_pages("documents/sample.pdf")

print("\nPage-wise PDF Test")
print("Total pages:", len(pages))

for page in pages:
    print("\nSource:", page["source"])
    print("Page:", page["page"])
    print("Text:", page["text"][:100])
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> dict:
    document = fitz.open(file_path)
    extracted_pages = []

    for page_number in range(len(document)):
        page = document.load_page(page_number)
        text = page.get_text()

        extracted_pages.append({
            "page_number": page_number + 1,
            "text": text.strip()
        })

    document.close()

    return {
        "total_pages": len(extracted_pages),
        "pages": extracted_pages
    }

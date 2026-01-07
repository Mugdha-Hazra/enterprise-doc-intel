import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> dict: # Function to extract text from a PDF file
    document = fitz.open(file_path) # Open the PDF document
    extracted_pages = [] # List to hold extracted text from each page

    for page_number in range(len(document)): # Iterate through each page in the PDF
        page = document.load_page(page_number) # Load the specific page
        text = page.get_text() # Extract text from the page

        extracted_pages.append({ # Append extracted text and page number to the list
            "page_number": page_number + 1, # Page numbers are 1-indexed
            "text": text.strip() # Strip leading/trailing whitespace
        })

    document.close() # Close the PDF document

    return { # Return a dictionary with total pages and extracted text
        "total_pages": len(extracted_pages), # Total number of pages in the PDF
        "pages": extracted_pages # List of extracted text from each page
    }
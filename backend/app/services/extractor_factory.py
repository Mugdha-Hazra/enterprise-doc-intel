import fitz # PyMuPDF
from app.services.base_extractor import TextExtractor # Import the base extractor class

class PDFTextExtractor(TextExtractor): # Concrete implementation of TextExtractor for PDF files

    def extract(self, file_path: str) -> dict: # Implement the extract method for PDF files
        document = fitz.open(file_path) # Open the PDF document
        pages = []

        for i in range(len(document)): # Iterate through each page in the PDF
            page = document.load_page(i) # Load the specific page
            pages.append({ # Append extracted text and page number to the list
                "page_number": i + 1,
                "text": page.get_text().strip() # Extract and strip text from the page
            })

        document.close() # Close the PDF document

        return { # Return a dictionary with total pages and extracted text
            "total_pages": len(pages),
            "pages": pages
        }
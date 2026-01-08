from abc import ABC, abstractmethod # Importing ABC and abstractmethod for defining an abstract base class for text extractors

class TextExtractor(ABC): # Define an abstract base class for text extractors

    @abstractmethod # Mark the extract method as abstract
    def extract(self, file_path: str) -> dict: # Abstract method to extract text from a file given its path
        pass # Placeholder for subclasses to implement the extraction logic
# app/services/chunking_service.py

class ChunkingService:
    """
    Splits text into chunks of ~500 characters.
    """
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk(self, text: str):
        chunks = []
        for i in range(0, len(text), self.chunk_size):
            chunks.append(text[i:i+self.chunk_size])
        return chunks

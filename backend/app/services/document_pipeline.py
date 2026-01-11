# app/services/document_pipeline.py

from app.services.pdf_service import PDFService
from app.services.chunking_service import ChunkingService
from app.search.embeddings import EmbeddingService
from app.search.faiss_index import FaissIndex


class DocumentPipeline:
    """
    Orchestrates:
    PDF → Text → Chunks → Embeddings → FAISS index
    """

    def __init__(self):
        self.pdf_service = PDFService()
        self.chunker = ChunkingService()
        self.embedder = EmbeddingService()
        self.index = FaissIndex(dim=384)

    def process(self, file_path: str) -> dict:
        # 1. Extract text
        text = self.pdf_service.extract_text(file_path)

        if not text or not text.strip():
            return {"text": None}

        # 2. Chunk text
        chunks = self.chunker.chunk(text)

        # 3. Generate embeddings
        embeddings = self.embedder.embed_documents(chunks)

        # 4. Store in FAISS
        for chunk, vector in zip(chunks, embeddings):
            self.index.add(vector, {"chunk_text": chunk})

        return {
            "text": text,
            "chunks": len(chunks)
        }

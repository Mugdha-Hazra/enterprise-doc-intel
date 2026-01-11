# app/services/rag_service.py

from app.search.embeddings import EmbeddingService
from app.search.faiss_index import FaissIndex


class RAGService:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.index = FaissIndex(dim=384)
        self.llm = None  # intentionally disabled

    def query(self, query: str, top_k: int = 5):
        query_vector = self.embedder.embed_query(query)

        results = self.index.search(query_vector, top_k)

        if not results:
            return {
                "answer": "No relevant documents found.",
                "sources": []
            }

        contexts = [r["chunk_text"] for r in results]

        answer = (
            "LLM disabled. Returning retrieved context only."
        )

        return {
            "answer": answer,
            "sources": results
        }

    # def set_llm(self, llm):
    #     self.llm = llm

    # def get_llm(self):
    #     return self.llm

    # def set_index(self, index):
    #     self.index = index

    # def get_index(self):
    #     return self.index

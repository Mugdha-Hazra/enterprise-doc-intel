# app/search/embeddings.py

from typing import List
import numpy as np

class EmbeddingService:
    def __init__(self):
        # placeholder dimension for embedding vector
        self.dim = 384

    def embed_query(self, query: str):
        """
        Returns a vector representation of a query string
        """
        # TODO: Replace with real embedding model (OpenAI, HuggingFace, etc.)
        return np.random.rand(self.dim).astype(np.float32)

    def embed_documents(self, docs: List[str]):
        """
        Returns a list of embeddings for documents/chunks
        """
        embeddings = []
        for doc in docs:
            # For now, random vectors — replace with real model
            embeddings.append(np.random.rand(self.dim).astype(np.float32))
        return embeddings

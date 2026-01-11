# app/search/faiss_index.py

import faiss
import numpy as np


class FaissIndex:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, vector, metadata: dict):
        vector = np.array([vector]).astype("float32")
        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, query_vector, top_k: int = 5):
        if self.index.ntotal == 0 or not self.metadata:
            return []

        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx, score in zip(indices[0], distances[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue

            item = self.metadata[idx].copy()
            item["score"] = float(score)
            results.append(item)

        return results

# app/routes/search.py

from fastapi import APIRouter
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/v1", tags=["Search"])

rag_service = RAGService()


@router.post("/search")
def rag_search(query: str, top_k: int = 5):
    return rag_service.query(query=query, top_k=top_k)

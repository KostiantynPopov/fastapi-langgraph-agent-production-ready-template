from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field
import httpx
from ...core.config import settings

class RAGQuerySchema(BaseModel):
    text: str = Field(..., description="Query text for RAG search")
    k: int = Field(5, description="Number of top results to return")
    # Можно добавить filters при необходимости

class RAGSearch(BaseTool):
    name = "rag_search"
    description = "Поиск фрагментов в базе знаний"
    args_schema = RAGQuerySchema

    async def _arun(self, text: str, k: int = 5, **kwargs):
        async with httpx.AsyncClient(timeout=20) as c:
            resp = await c.post(f"{settings.RAG_URL}/collections/{settings.RAG_COLLECTION_ID}/documents/search",
                                json={"query": text, "top_k": k})
            resp.raise_for_status()
        return resp.json()

class RAGIngestSchema(BaseModel):
    file_url: str = Field(..., description="URL файла для загрузки в RAG")
    # Можно добавить другие поля (например, метаданные)

class RAGIngest(BaseTool):
    name = "rag_ingest"
    description = "Загрузка новых документов в базу знаний RAG"
    args_schema = RAGIngestSchema

    async def _arun(self, file_url: str, **kwargs):
        async with httpx.AsyncClient(timeout=60) as c:
            resp = await c.post(f"{settings.RAG_URL}/collections/{settings.RAG_COLLECTION_ID}/documents",
                                json={"file_url": file_url})
            resp.raise_for_status()
        return resp.json()

rag_search_tool = RAGSearch()
rag_ingest_tool = RAGIngest() 
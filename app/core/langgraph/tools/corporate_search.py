from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field
import httpx

# Креды и параметры RAG
LANGCONNECT_BASE_URL = "http://langconnect-api:8080"
LANGCONNECT_TOKEN = "user1"
LANGCONNECT_COLLECTION_ID = "1eea8486-74b5-4749-b742-60b4b7a3230e"
DEFAULT_HTTP_TIMEOUT = 10

class CorporateSearchArgs(BaseModel):
    query: str = Field(..., description="Строка запроса пользователя")
    limit: int = Field(10, description="Максимум фрагментов (по умолчанию 5)")

class CorporateSearchTool(BaseTool):
    name: str = "corporate_search"
    description: str = "Получить релевантные фрагменты из корпоративного RAG (LangConnect) по пользовательскому запросу."
    args_schema: type = CorporateSearchArgs

    async def _arun(self, query: str, limit: int = 5):
        url = f"{LANGCONNECT_BASE_URL.rstrip('/')}/collections/{LANGCONNECT_COLLECTION_ID}/documents/search"
        headers = {
            "Authorization": f"Bearer {LANGCONNECT_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
        }
        try:
            async with httpx.AsyncClient(timeout=DEFAULT_HTTP_TIMEOUT) as client:
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
        except httpx.HTTPError as exc:
            return f"Ошибка: не удалось получить данные из корпоративного хранилища. {exc}"
        data = resp.json()
        if isinstance(data, list):
            results = data
        else:
            results = data.get("results", [])
        if not results:
            return "По запросу ничего не найдено."
        chunks = []
        for hit in results[:limit]:
            text = (hit.get("page_content") or hit.get("text") or hit.get("chunk") or "").strip()
            meta = hit.get("metadata", {})
            source = meta.get("source") or meta.get("file_name") or meta.get("document_id")
            score = hit.get("score") or hit.get("similarity")
            fragment = text
            if source:
                fragment = f"[{source}] {fragment}"
            if score is not None:
                fragment = f"(score≈{score:.3f}) {fragment}"
            chunks.append(fragment)
        return "\n\n".join(chunks)

    def _run(self, query: str, limit: int = 5):
        raise NotImplementedError("Только асинхронный режим (_arun) поддерживается.")

corporate_search_tool = CorporateSearchTool() 
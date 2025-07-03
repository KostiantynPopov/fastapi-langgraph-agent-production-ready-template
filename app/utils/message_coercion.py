import json
from typing import Any

def to_message(content: Any) -> str:
    """Преобразует content (str или dict) в строку для передачи в LangChain."""
    if isinstance(content, dict):
        return "__filemsg__" + json.dumps(content, ensure_ascii=False)
    return content

def from_message(content: str) -> Any:
    """Преобразует строку обратно в dict, если это сериализованный file-message."""
    if isinstance(content, str) and content.startswith("__filemsg__"):
        try:
            return json.loads(content[len("__filemsg__"):])
        except Exception:
            return content
    return content 
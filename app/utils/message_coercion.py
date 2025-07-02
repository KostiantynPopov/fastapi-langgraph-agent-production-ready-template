from typing import Any, Dict, Union

from langchain_core.messages import BaseMessage
from app.schemas import Message

# Map LangChain's internal `.type` → your public `.role`
ROLE_MAP: Dict[str, str] = {
    "human": "user",
    "ai": "assistant",
    "system": "system",
    "tool": "assistant",          # adjust if you keep a separate "tool" role
}


def to_message(obj: Union[Message, BaseMessage, Dict[str, Any], str]) -> Message:
    """Convert anything that can appear in the history into `Message`."""
    # Already good
    if isinstance(obj, Message):
        return obj

    # LangChain objects (`HumanMessage`, `AIMessage`, `SystemMessage`, …)
    if isinstance(obj, BaseMessage):
        role = ROLE_MAP.get(getattr(obj, "type", "user"), "user")
        return Message(role=role, content=obj.content)

    # OpenAI-style dict {"role": "...", "content": ...}
    if isinstance(obj, dict) and "content" in obj:
        return Message(role=obj.get("role", "user"), content=obj["content"])

    # Raw string – treat as a user message
    if isinstance(obj, str):
        return Message(role="user", content=obj)

    raise TypeError(f"Unsupported message object: {type(obj)}") 
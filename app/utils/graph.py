"""This file contains the graph utilities for the application."""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import trim_messages as _trim_messages
from typing import Any

from app.core.config import settings
from app.schemas import Message
from app.utils.message_coercion import to_message


def serialize_content(content):
    """Преобразует content (dict или str) в строку для LLM."""
    if isinstance(content, dict):
        text = content.get("text", "")
        file = content.get("file")
        file_str = ""
        if file:
            file_str = f"\n[Файл: {file.get('name', '')} ({file.get('extension', '')}), размер: {file.get('size', 0)} байт]"
        return (text or "") + file_str
    return content


def dump_messages(messages: list[Message]) -> list[dict]:
    """Dump the messages to a list of dictionaries.

    Args:
        messages (list[Message]): The messages to dump.

    Returns:
        list[dict]: The dumped messages.
    """
    # Для истории сохраняем оригинальный content, для LLM сериализуем
    return [
        {**message.model_dump(), "content": serialize_content(message.content)}
        for message in messages
    ]


def prepare_messages(
    messages: list[Any],        # NOTE: now accepts *anything*
    llm: BaseChatModel,
    system_prompt: str,
) -> list[Message]:
    """Ensure we work only with `Message`, trim for context window, prepend system."""
    # 1. Normalise *everything* first
    internal = [to_message(m) for m in messages]

    # 2. Token-based trimming (works on dicts)
    trimmed = _trim_messages(
        dump_messages(internal),   # dump_messages expects `Message` → dict
        strategy="last",
        token_counter=llm,
        max_tokens=settings.MAX_TOKENS,
        start_on="human",
        include_system=False,
        allow_partial=False,
    )

    # 3. Bring the trimmed slice back to `Message`
    trimmed_internal = [to_message(m) for m in trimmed]

    # 4. Finally prepend system-prompt
    return [Message(role="system", content=system_prompt)] + trimmed_internal

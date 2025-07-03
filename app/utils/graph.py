"""This file contains the graph utilities for the application."""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import trim_messages as _trim_messages

from app.core.config import settings
from app.schemas import Message
from .message_coercion import to_message


def dump_messages(messages: list) -> list:
    """Преобразует сообщения в формат, пригодный для передачи в LLM (content всегда str)."""
    result = []
    for msg in messages:
        msg_dict = msg.model_dump() if hasattr(msg, 'model_dump') else dict(msg)
        msg_dict = dict(msg_dict)  # ensure mutable
        msg_dict["content"] = to_message(msg_dict["content"])
        result.append(msg_dict)
    return result


def prepare_messages(messages: list[Message], llm: BaseChatModel, system_prompt: str) -> list[Message]:
    """Prepare the messages for the LLM.

    Args:
        messages (list[Message]): The messages to prepare.
        llm (BaseChatModel): The LLM to use.
        system_prompt (str): The system prompt to use.

    Returns:
        list[Message]: The prepared messages.
    """
    trimmed_messages = _trim_messages(
        dump_messages(messages),
        strategy="last",
        token_counter=llm,
        max_tokens=settings.MAX_TOKENS,
        start_on="human",
        include_system=False,
        allow_partial=False,
    )
    return [Message(role="system", content=system_prompt)] + trimmed_messages

"""This file contains the chat schema for the application."""

import re
from typing import (
    List,
    Literal,
    Any,
)

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class Message(BaseModel):
    """Message model for chat endpoint.

    Attributes:
        role: The role of the message sender (user or assistant).
        content: The content of the message.
    """

    model_config = {"extra": "ignore"}

    role: Literal["user", "assistant", "system"] = Field(..., description="The role of the message sender")
    content: Any = Field(..., description="The content of the message (str or dict)")

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: Any) -> Any:
        if isinstance(v, str):
            # Check for potentially harmful content
            if re.search(r"<script.*?>.*?</script>", v, re.IGNORECASE | re.DOTALL):
                raise ValueError("Content contains potentially harmful script tags")
            # Check for null bytes
            if "\0" in v:
                raise ValueError("Content contains null bytes")
            return v
        elif isinstance(v, dict):
            text = v.get("text", "")
            if not isinstance(text, str):
                raise ValueError("Field 'text' in content dict must be a string")
            if re.search(r"<script.*?>.*?</script>", text, re.IGNORECASE | re.DOTALL):
                raise ValueError("Content.text contains potentially harmful script tags")
            if "\0" in text:
                raise ValueError("Content.text contains null bytes")
            # file может быть любым объектом/None
            return v
        else:
            raise ValueError("Content must be either a string or a dict with 'text' and/or 'file'")


class ChatRequest(BaseModel):
    """Request model for chat endpoint.

    Attributes:
        messages: List of messages in the conversation.
        entity_id: Optional external entity identifier (e.g., Bitrix24 CHAT_ENTITY_ID)
    """

    messages: List[Message] = Field(
        ...,
        description="List of messages in the conversation",
        min_length=1,
    )
    entity_id: str | None = Field(default=None, description="External entity ID (e.g., Bitrix24 CHAT_ENTITY_ID)")


class ChatResponse(BaseModel):
    """Response model for chat endpoint.

    Attributes:
        messages: List of messages in the conversation.
    """

    messages: List[Message] = Field(..., description="List of messages in the conversation")


class StreamResponse(BaseModel):
    """Response model for streaming chat endpoint.

    Attributes:
        content: The content of the current chunk.
        done: Whether the stream is complete.
    """

    content: str = Field(default="", description="The content of the current chunk")
    done: bool = Field(default=False, description="Whether the stream is complete")

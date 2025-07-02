"""LangGraph tools for enhanced language model capabilities.

This package contains custom tools that can be used with LangGraph to extend
the capabilities of language models. Currently includes tools for web search
and other external integrations.
"""

from langchain_core.tools.base import BaseTool

from .duckduckgo_search import duckduckgo_search_tool
from .general import city_time_tool
from .bitrix import bitrix_find_contact_by_entity_id_tool
from .corporate_search import corporate_search_tool
from .click_knock import (
    upload_file_tool,
    create_order_tool,
    create_task_tool,
    attach_file_tool,
    update_task_tool,
)


tools: list = [
    duckduckgo_search_tool,
    corporate_search_tool,
    city_time_tool,
    bitrix_find_contact_by_entity_id_tool,
    upload_file_tool,
    create_order_tool,
    create_task_tool,
    attach_file_tool,
    update_task_tool,
]

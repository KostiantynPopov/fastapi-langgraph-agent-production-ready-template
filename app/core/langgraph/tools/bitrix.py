import os
import requests
import time
import logging
from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field

BITRIX_WEBHOOK = os.environ.get("BITRIX_WEBHOOK")
LOGGER = logging.getLogger(__name__)

def _retry_post(url: str, json_payload: dict, max_retries: int = 3, timeout: int = 10) -> requests.Response:
    retries = 0
    while retries < max_retries:
        try:
            resp = requests.post(url, json=json_payload, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as exc:
            retries += 1
            wait = 2 ** retries
            LOGGER.warning(f"Bitrix request failed (%s). Retry %s/%s in %ss…", exc, retries, max_retries, wait)
            time.sleep(wait)
    raise RuntimeError(f"Exceeded {max_retries} retries calling {url}")


class BitrixContactByEntityIdArgs(BaseModel):
    entity_id: str = Field(..., description="Bitrix24 CHAT_ENTITY_ID, e.g. 'telegrambot|19|442236029|18'")

class BitrixFindContactByEntityIdTool(BaseTool):
    name: str = "bitrix_find_contact_by_entity_id"
    description: str = "Find Bitrix24 contact by messenger entity_id (searches by IM field with 'imol|' prefix)."
    args_schema: type = BitrixContactByEntityIdArgs

    def _run(self, entity_id: str):
        if not BITRIX_WEBHOOK:
            return "BITRIX_WEBHOOK env variable is not set."
        im_value = f"imol|{entity_id}"
        payload = {'filter': {'IM': im_value}}
        try:
            url = f"{BITRIX_WEBHOOK}/crm.contact.list.json"
            resp = _retry_post(url, payload)
            data = resp.json()
            contacts = data.get('result', [])
            if contacts:
                return contacts[0]
            return f"No contact found for entity_id: {entity_id}"
        except Exception as e:
            return f"Error searching contact by entity_id: {e}"

bitrix_find_contact_by_entity_id_tool = BitrixFindContactByEntityIdTool()

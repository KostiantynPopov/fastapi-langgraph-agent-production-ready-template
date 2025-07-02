"""Click-Knock integration tools for LangGraph."""

from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field
import httpx
from typing import List

BASE = "https://api.click-knock.com/api/v1"

class UploadFileArgs(BaseModel):
    filename: str
    content_b64: str

class UploadFileTool(BaseTool):
    name: str = "ck_upload_file"
    description: str = "Upload a file to Click-Knock. Args: filename, content_b64 (base64-encoded file)"
    args_schema: type = UploadFileArgs

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Use async version (_arun)")

    async def _arun(self, filename: str, content_b64: str):
        files = {"file": (filename, content_b64)}
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE}/upload", files=files)
            r.raise_for_status()
            return r.json()

upload_file_tool = UploadFileTool()

class CreateOrderArgs(BaseModel):
    flow: str = "common"
    status: int = 0
    communication_type: List[str] = ["phone"]

class CreateOrderTool(BaseTool):
    name: str = "ck_create_order"
    description: str = "Create a new Click-Knock order. Args: flow, status, communication_type"
    args_schema: type = CreateOrderArgs

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Use async version (_arun)")

    async def _arun(self, flow: str = "common", status: int = 0, communication_type: List[str] = ["phone"]):
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE}/orders", json={"flow": flow, "status": status, "communication_type": communication_type})
            r.raise_for_status()
            return r.json()

create_order_tool = CreateOrderTool()

class CreateTaskArgs(BaseModel):
    order_slug: str
    product_type: str
    printing: dict
    postprint: dict
    sheets_amount: int = 1
    products_amount: int = 1

class CreateTaskTool(BaseTool):
    name: str = "ck_create_task"
    description: str = "Create a print task in Click-Knock. Args: order_slug, product_type, printing, postprint, sheets_amount, products_amount"
    args_schema: type = CreateTaskArgs

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Use async version (_arun)")

    async def _arun(self, order_slug: str, product_type: str, printing: dict, postprint: dict, sheets_amount: int = 1, products_amount: int = 1):
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE}/order-tasks", json={
                "order_slug": order_slug,
                "product_type": product_type,
                "printing": printing,
                "postprint": postprint,
                "sheets_amount": sheets_amount,
                "products_amount": products_amount,
            })
            r.raise_for_status()
            return r.json()

create_task_tool = CreateTaskTool()

class AttachFileArgs(BaseModel):
    id: str
    copies: int
    order_task_slug: str

class AttachFileTool(BaseTool):
    name: str = "ck_attach_file"
    description: str = "Attach a file to a Click-Knock order task. Args: id (file id), copies, order_task_slug"
    args_schema: type = AttachFileArgs

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Use async version (_arun)")

    async def _arun(self, id: str, copies: int, order_task_slug: str):
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE}/order-task-files", json={
                "id": id,
                "copies": copies,
                "order_task_slug": order_task_slug,
            })
            r.raise_for_status()
            return r.json()

attach_file_tool = AttachFileTool()

class UpdateTaskArgs(BaseModel):
    order_slug: str
    task_slug: str
    printing: dict
    postprint: dict

class UpdateTaskTool(BaseTool):
    name: str = "ck_update_task"
    description: str = "Update a Click-Knock order task. Args: order_slug, task_slug, printing, postprint"
    args_schema: type = UpdateTaskArgs

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Use async version (_arun)")

    async def _arun(self, order_slug: str, task_slug: str, printing: dict, postprint: dict):
        async with httpx.AsyncClient() as client:
            r = await client.put(f"{BASE}/order-tasks/{task_slug}", json={
                "order_slug": order_slug,
                "task_slug": task_slug,
                "printing": printing,
                "postprint": postprint,
            })
            r.raise_for_status()
            return r.json()

update_task_tool = UpdateTaskTool()

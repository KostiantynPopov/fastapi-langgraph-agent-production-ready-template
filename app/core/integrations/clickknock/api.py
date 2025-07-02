import httpx
from pydantic import BaseModel, Field
from typing import Optional, List

BASE = "https://api.click-knock.com/api/v1"

class UploadFileArgs(BaseModel):
    filename: str
    content_b64: str  # base64-encoded file content

async def upload_file(args: UploadFileArgs) -> dict:
    files = {"file": (args.filename, args.content_b64)}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/upload", files=files)
        r.raise_for_status()
        return r.json()

class CreateOrderArgs(BaseModel):
    flow: str = "common"
    status: int = 0
    communication_type: List[str] = ["phone"]

async def create_order(args: CreateOrderArgs) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/orders", json=args.dict())
        r.raise_for_status()
        return r.json()

class CreateTaskArgs(BaseModel):
    order_slug: str
    product_type: str
    printing: dict
    postprint: dict
    sheets_amount: int = 1
    products_amount: int = 1

async def create_task(args: CreateTaskArgs) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/order-tasks", json=args.dict())
        r.raise_for_status()
        return r.json()

class AttachFileArgs(BaseModel):
    id: str
    copies: int
    order_task_slug: str

async def attach_file(args: AttachFileArgs) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/order-task-files", json=args.dict())
        r.raise_for_status()
        return r.json()

class UpdateTaskArgs(BaseModel):
    order_slug: str
    task_slug: str
    printing: dict
    postprint: dict

async def update_task(args: UpdateTaskArgs) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{BASE}/order-tasks/{args.task_slug}", json=args.dict())
        r.raise_for_status()
        return r.json() 
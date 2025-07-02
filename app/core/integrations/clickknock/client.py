from typing import Dict, Any, Optional
from .base import BaseAPIClient
import os

class ClickKnockAPIClient(BaseAPIClient):
    """API client for Click-Knock system."""
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        super().__init__(base_url, api_key, timeout)

    def update_order_task(
        self,
        order_slug: str,
        task_slug: str,
        printing_data: Optional[Dict[str, Any]] = None,
        postprint_data: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an order task in Click-Knock system."""
        endpoint = f"/api/v1/orders/{order_slug}/tasks/{task_slug}"
        data = {}
        if printing_data is not None:
            data["printing"] = printing_data
        if postprint_data is not None:
            data["postprint"] = postprint_data
        headers = None
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        return self.put(endpoint, data=data, headers=headers)


def update_order_task(
    order_slug: str,
    task_slug: str,
    printing_data: Optional[Dict[str, Any]] = None,
    postprint_data: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an order task in Click-Knock system.
    Args:
        order_slug: Order slug
        task_slug: Task slug
        printing_data: Printing data
        postprint_data: Postprint data
        token: Optional access token
    Returns:
        Dict[str, Any]: Update result
    """
    base_url = os.getenv("CK_API_BASE_URL", "https://api.click-knock.com/")
    api_key = os.getenv("CK_API_KEY")
    timeout = int(os.getenv("CK_API_TIMEOUT", "30"))
    client = ClickKnockAPIClient(base_url, api_key, timeout)
    return client.update_order_task(
        order_slug=order_slug,
        task_slug=task_slug,
        printing_data=printing_data,
        postprint_data=postprint_data,
        token=token,
    )


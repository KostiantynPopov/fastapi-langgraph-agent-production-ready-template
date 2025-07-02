from .base import BaseAPIClient
from typing import Optional
import os


def get_token(phone_number: str, password: str, base_url: Optional[str] = None, timeout: Optional[int] = None) -> str:
    """Get access token from Click-Knock API by phone and password."""
    base_url = base_url or os.getenv("CK_API_BASE_URL", "https://api.click-knock.com/")
    timeout = timeout or int(os.getenv("CK_API_TIMEOUT", "30"))
    client = BaseAPIClient(base_url, timeout=timeout)
    url = f"{base_url}/auth/access-token"
    data = {"phone_number": phone_number, "password": password}
    import requests
    response = requests.post(url, data=data, timeout=timeout)
    response.raise_for_status()
    token = response.json().get("accessToken") or response.json().get("access_token")
    if not token:
        raise Exception(f"Failed to get token: {response.text}")
    return token
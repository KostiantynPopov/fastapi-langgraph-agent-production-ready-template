"""Base API client for HTTP requests."""

import requests
from typing import Any, Dict, Optional
from requests.exceptions import RequestException

class BaseAPIClient:
    """Base class for API clients."""
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"API request error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Server response: {e.response.text}")
            raise RequestException(f"API request error: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("POST", endpoint, data=data, params=params, headers=headers)

    def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("PUT", endpoint, data=data, params=params, headers=headers)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("DELETE", endpoint, params=params, headers=headers)

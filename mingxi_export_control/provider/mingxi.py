"""MingXi Export Control API provider - credential validation."""
import requests
from dify_plugin import ToolProvider


class MingXiProvider(ToolProvider):
    """Provider for MingXi Export Control API.

    Validates the user's API key by making a lightweight request
    to the MingXi balance endpoint.
    """

    def validate_credentials(self, credentials: dict) -> None:
        api_key = credentials.get("api_key")
        if not api_key or not api_key.startswith("sk-"):
            raise ValueError("Invalid API key format. Key should start with 'sk-'.")

        try:
            resp = requests.get(
                "https://api.mingxiapi.cn/v1/balance",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10,
            )
            if resp.status_code in (403, 404):
                raise ValueError("API key is invalid or banned.")
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to connect to MingXi API: {e}")

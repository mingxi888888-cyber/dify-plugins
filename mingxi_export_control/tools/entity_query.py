"""Tool: Query China's restricted entity lists."""
import requests
from dify_plugin import Tool


class EntityQueryTool(Tool):
    """Query the MingXi restricted entity database."""

    def _invoke(self, tool_parameters: dict) -> dict:
        api_key = self.runtime.credentials.get("api_key")
        keyword = tool_parameters.get("keyword", "")
        fmt = tool_parameters.get("format", "json")

        if not keyword:
            return {"error": "keyword is required"}

        try:
            resp = requests.post(
                "https://api.mingxiapi.cn/v1/query",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "keyword": keyword,
                    "api_key": api_key,
                    "dataset": "entity",
                    "format": fmt,
                },
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError:
            if resp.status_code == 403:
                return {"error": "API key invalid or balance insufficient"}
            return {"error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}

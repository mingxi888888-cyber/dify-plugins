"""Tool: Query China's dual-use export control items."""
import requests
from dify_plugin import Tool


class ItemQueryTool(Tool):
    """Query the MingXi Export Control dual-use item database."""

    def _invoke(self, tool_parameters: dict) -> dict:
        api_key = self.runtime.credentials.get("api_key")
        keyword = tool_parameters.get("keyword", "")
        top_k = int(tool_parameters.get("top_k", 5))
        fmt = tool_parameters.get("format", "json")

        if not keyword:
            return {"error": "keyword is required"}

        top_k = max(1, min(top_k, 20))

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
                    "dataset": "export_control",
                    "top_k": top_k,
                    "format": fmt,
                },
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 403:
                return {"error": "API key invalid or balance insufficient"}
            return {"error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}

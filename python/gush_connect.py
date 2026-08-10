---

### **2. `python/gush_connect.py`**

Create a folder named `python` and add `gush_connect.py`:

```python
"""
Gush Connect Python SDK v1.0
Official Python client library for Gush AI Agent Workspace (https://ai.sstore.ng/)
"""

import json
import logging
from typing import Any, Dict, Optional
import requests

logging.basicConfig(level=logging.INFO)

class GushConnectClient:
    def __init__(self, workspace_url: str = "https://ai.sstore.ng/", auth_token: Optional[str] = None):
        self.workspace_url = workspace_url.rstrip("/") + "/"
        self.auth_token = auth_token
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "GushConnect-PythonSDK/1.0"
        })
        if self.auth_token:
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})

    def trigger_agent_task(
        self,
        prompt: str,
        mode: str = "general",
        model: str = "gemini::gemini-2.5-flash",
        search_pref: str = "allow",
        project_id: int = 0
    ) -> Dict[str, Any]:
        """
        Dispatches a user or automated prompt to the Gush AI Agent engine.
        """
        endpoint = f"{self.workspace_url}?action="
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "mode": mode,
            "model": model,
            "search_pref": search_pref,
            "project_id": project_id
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=90)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Gush Connect Request Error: {e}")
            return {"ok": False, "error": str(e)}

    def execute_integration_tool(self, tool_id: int, integration_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a registered user API integration tool programmatically.
        """
        endpoint = f"{self.workspace_url}?action=test_user_integration_tool"
        payload = {
            "tool_id": tool_id,
            "integration_id": integration_id,
            "params": params or {}
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=45)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Tool Execution Error: {e}")
            return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    # Starter Verification Execution
    client = GushConnectClient()
    res = client.trigger_agent_task("System Status Check via Gush Connect SDK.")
    print("Execution Result:", json.dumps(res, indent=2))

# Gush-connect

# Gush Connect SDK & Integration Hub

Official open-source developer SDKs and background execution connectors for **Gush AI Agent Workspace** ([https://ai.sstore.ng/](https://ai.sstore.ng/)).

Gush Connect bridges custom business logic, E-commerce APIs (Shopify, WooCommerce), CRMs, and internal database microservices with Gush AI's autonomous agent framework.

---

### Key Features

*   **Multi-Language SDKs**: Python, JavaScript/Node.js, and Go client libraries.
*   **Tool Dispatching**: Execute background agent tasks and trigger external API endpoints programmatically.
*   **Zero-Exposure Key Handling**: Secure server-side credential isolation for API keys and Bearer tokens.
*   **OpenAPI 3.0 Auto-Discovery**: Convert standard Swagger/OpenAPI schemas into executable agent tools.

---

### Quickstart Example (Python)

```python
from python.gush_connect import GushConnectClient

client = GushConnectClient(
    workspace_url="https://ai.sstore.ng/",
    auth_token="YOUR_SESSION_OR_API_KEY"
)

# Programmatically trigger an autonomous agent workflow
response = client.trigger_agent_task(
    prompt="Fetch today's completed sales orders and summarize revenue.",
    search_pref="allow"
)

print("Agent Response:", response.get("reply"))

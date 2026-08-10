/**
 * Gush Connect JavaScript / Node.js SDK v1.0
 * Official JS client library for Gush AI Agent Workspace (https://ai.sstore.ng/)
 */

class GushConnectClient {
  constructor(options = {}) {
    this.workspaceUrl = (options.workspaceUrl || 'https://ai.sstore.ng/').replace(/\/+$/, '') + '/';
    this.authToken = options.authToken || null;
  }

  /**
   * Helper method to send JSON HTTP requests
   */
  async _request(action, payload = {}) {
    const url = `${this.workspaceUrl}?action=${action}`;
    const headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'GushConnect-JSSDK/1.0'
    };

    if (this.authToken) {
      headers['Authorization'] = `Bearer ${this.authToken}`;
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP Error ${response.status}: ${errorText}`);
      }

      return await response.json();
    } catch (err) {
      return { ok: false, error: err.message };
    }
  }

  /**
   * Dispatch prompt task to Gush AI Agent
   */
  async triggerAgentTask(prompt, config = {}) {
    const payload = {
      messages: [{ role: 'user', content: prompt }],
      mode: config.mode || 'general',
      model: config.model || 'gemini::gemini-2.5-flash',
      search_pref: config.searchPref || 'allow',
      project_id: config.projectId || 0
    };

    return await this._request('', payload);
  }

  /**
   * Execute registered user API tool
   */
  async executeTool(toolId, integrationId, params = {}) {
    return await this._request('test_user_integration_tool', {
      tool_id: toolId,
      integration_id: integrationId,
      params
    });
  }
}

// Export for ES modules and Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GushConnectClient };
}

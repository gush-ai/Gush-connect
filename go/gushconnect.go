/*
Package gushconnect provides the official Go SDK for Gush AI Agent Workspace (https://ai.sstore.ng/).
*/
package gushconnect

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

type Client struct {
	BaseURL    string
	AuthToken  string
	HTTPClient *http.Client
}

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type TaskRequest struct {
	Messages   []Message `json:"messages"`
	Mode       string    `json:"mode,omitempty"`
	Model      string    `json:"model,omitempty"`
	SearchPref string    `json:"search_pref,omitempty"`
	ProjectID  int       `json:"project_id,omitempty"`
}

type TaskResponse struct {
	OK      bool   `json:"ok"`
	Reply   string `json:"reply"`
	Model   string `json:"model"`
	Error   string `json:"error,omitempty"`
}

func NewClient(baseURL, authToken string) *Client {
	if baseURL == "" {
		baseURL = "https://ai.sstore.ng/"
	}
	if !strings.HasSuffix(baseURL, "/") {
		baseURL += "/"
	}
	return &Client{
		BaseURL:   baseURL,
		AuthToken: authToken,
		HTTPClient: &http.Client{
			Timeout: 90 * time.Second,
		},
	}
}

func (c *Client) TriggerAgentTask(prompt string) (*TaskResponse, error) {
	reqURL := fmt.Sprintf("%s?action=", c.BaseURL)
	payload := TaskRequest{
		Messages: []Message{
			{Role: "user", Content: prompt},
		},
		Mode:       "general",
		SearchPref: "allow",
	}

	jsonBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", reqURL, bytes.NewBuffer(jsonBytes))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "GushConnect-GoSDK/1.0")
	if c.AuthToken != "" {
		req.Header.Set("Authorization", "Bearer "+c.AuthToken)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var taskResp TaskResponse
	err = json.Unmarshal(body, &taskResp)
	if err != nil {
		return nil, err
	}

	return &taskResp, nil
}

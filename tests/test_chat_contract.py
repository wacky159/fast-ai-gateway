"""
Contract tests for the chat endpoint.
"""

from fastapi.testclient import TestClient


def test_chat_returns_200(client: TestClient) -> None:
    """Test that POST /v1/chat returns 200 status code."""
    response = client.post(
        "/v1/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )
    assert response.status_code == 200


def test_chat_response_has_required_fields(client: TestClient) -> None:
    """Test that chat response contains all required fields."""
    response = client.post(
        "/v1/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )
    data = response.json()

    assert "id" in data
    assert "provider" in data
    assert "model" in data
    assert "output" in data
    assert "usage" in data


def test_chat_usage_has_token_fields(client: TestClient) -> None:
    """Test that usage object has token fields."""
    response = client.post(
        "/v1/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )
    data = response.json()
    usage = data["usage"]

    assert "input_tokens" in usage
    assert "output_tokens" in usage
    assert "total_tokens" in usage


def test_chat_validates_empty_messages(client: TestClient) -> None:
    """Test that chat endpoint validates empty messages array."""
    response = client.post(
        "/v1/chat",
        json={
            "messages": [],
        },
    )
    assert response.status_code == 422


def test_chat_validates_missing_messages(client: TestClient) -> None:
    """Test that chat endpoint validates missing messages field."""
    response = client.post(
        "/v1/chat",
        json={},
    )
    assert response.status_code == 422


def test_chat_accepts_optional_parameters(client: TestClient) -> None:
    """Test that chat endpoint accepts optional parameters."""
    response = client.post(
        "/v1/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.5,
            "max_tokens": 100,
            "response_format": "json",
        },
    )
    assert response.status_code == 200

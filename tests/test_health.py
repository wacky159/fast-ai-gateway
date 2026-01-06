"""
Contract tests for the health endpoint.
"""

from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    """Test that GET /health returns 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_has_required_fields(client: TestClient) -> None:
    """Test that health response contains all required fields."""
    response = client.get("/health")
    data = response.json()

    assert "status" in data
    assert "provider" in data
    assert "model" in data
    assert "version" in data


def test_health_status_is_ok(client: TestClient) -> None:
    """Test that health status is 'ok'."""
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "ok"


def test_health_returns_correct_content_type(client: TestClient) -> None:
    """Test that health endpoint returns JSON content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]

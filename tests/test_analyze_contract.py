"""
Contract tests for the analyze endpoint.
"""

from fastapi.testclient import TestClient


def test_analyze_returns_200(client: TestClient) -> None:
    """Test that POST /v1/analyze returns 200 status code."""
    response = client.post(
        "/v1/analyze",
        json={
            "text": "This is a test text.",
        },
    )
    assert response.status_code == 200


def test_analyze_response_has_required_fields(client: TestClient) -> None:
    """Test that analyze response contains all required fields."""
    response = client.post(
        "/v1/analyze",
        json={
            "text": "This is a test text.",
        },
    )
    data = response.json()

    assert "provider" in data
    assert "model" in data
    assert "label" in data
    assert "score" in data
    assert "summary" in data
    assert "extras" in data


def test_analyze_validates_empty_text(client: TestClient) -> None:
    """Test that analyze endpoint validates empty text."""
    response = client.post(
        "/v1/analyze",
        json={
            "text": "",
        },
    )
    assert response.status_code == 422


def test_analyze_validates_missing_text(client: TestClient) -> None:
    """Test that analyze endpoint validates missing text field."""
    response = client.post(
        "/v1/analyze",
        json={},
    )
    assert response.status_code == 422


def test_analyze_accepts_options(client: TestClient) -> None:
    """Test that analyze endpoint accepts options."""
    response = client.post(
        "/v1/analyze",
        json={
            "text": "This is a test text.",
            "options": {
                "need_summary": True,
                "need_label": True,
                "need_score": True,
                "extra_fields": ["keywords", "category"],
            },
        },
    )
    assert response.status_code == 200


def test_analyze_score_is_valid_range(client: TestClient) -> None:
    """Test that score is within valid range when present."""
    response = client.post(
        "/v1/analyze",
        json={
            "text": "This is a test text.",
        },
    )
    data = response.json()

    if data["score"] is not None:
        assert 0.0 <= data["score"] <= 1.0


def test_analyze_label_is_string_or_null(client: TestClient) -> None:
    """Test that label is a string or null."""
    response = client.post(
        "/v1/analyze",
        json={
            "text": "This is a test text.",
        },
    )
    data = response.json()

    assert data["label"] is None or isinstance(data["label"], str)

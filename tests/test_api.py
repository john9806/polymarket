from fastapi.testclient import TestClient

from app import app


def test_recommendations_endpoint_returns_expected_shape() -> None:
    with TestClient(app) as client:
        response = client.get("/recommendations/u1?k=2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["user_id"] == "u1"
    assert isinstance(payload["recommendations"], list)
    assert len(payload["recommendations"]) <= 2
    if payload["recommendations"]:
        first = payload["recommendations"][0]
        assert "market_id" in first
        assert "score" in first

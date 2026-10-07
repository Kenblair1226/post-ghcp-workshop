import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize("path", ["/", "/tracking", "/health"])
def test_pages(client, path):
    assert client.get(path).status_code == 200


def test_quote(client):
    response = client.post("/api/quote", json={"weight_grams": 1000, "service": "standard"})
    assert response.status_code == 200
    assert response.json == {"fee": 60, "currency": "TWD"}


@pytest.mark.parametrize("payload", [[], None, {}, {"weight_grams": "1000", "service": "standard"}])
def test_invalid_json_payload(client, payload):
    response = client.post("/api/quote", json=payload)
    assert response.status_code == 400
    assert "error" in response.json


def test_malformed_json(client):
    response = client.post("/api/quote", data="{", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.json


def test_tracking(client):
    assert client.get("/api/tracking/DEMO0001").json["status"] == "已投遞"
    assert client.get("/api/tracking/MISSING").status_code == 404

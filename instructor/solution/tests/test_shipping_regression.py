import pytest

from app import create_app
from shipping import calculate_fee


@pytest.mark.parametrize(
    "weight,expected",
    [(1, 60), (1000, 60), (1001, 70), (2000, 70), (20000, 250)],
)
def test_weight_boundaries(weight, expected):
    assert calculate_fee(weight, "standard") == expected


@pytest.mark.parametrize("service,expected", [("standard", 60), ("registered", 80), ("express", 90)])
def test_service_fees(service, expected):
    assert calculate_fee(1000, service) == expected


@pytest.mark.parametrize("weight", [0, -1, 20001, 1.5, True, False, "1000", None])
def test_invalid_weight(weight):
    with pytest.raises(ValueError, match="重量"):
        calculate_fee(weight, "standard")


@pytest.mark.parametrize("service", ["unknown", "", None, [], True])
def test_invalid_service(service):
    with pytest.raises(ValueError, match="服務"):
        calculate_fee(1000, service)


@pytest.mark.parametrize("weight", [0, -1, 20001, 1.5, True, "1000", None])
def test_api_rejects_invalid_weight(weight):
    with create_app().test_client() as client:
        response = client.post("/api/quote", json={"weight_grams": weight, "service": "standard"})
    assert response.status_code == 400
    assert "error" in response.json
    assert "fee" not in response.json


def test_api_supports_express_at_maximum():
    with create_app().test_client() as client:
        response = client.post("/api/quote", json={"weight_grams": 20000, "service": "express"})
    assert response.status_code == 200
    assert response.json == {"fee": 280, "currency": "TWD"}

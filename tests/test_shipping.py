import pytest

from shipping import calculate_fee


@pytest.mark.parametrize(
    "weight,service,expected",
    [(500, "standard", 60), (1000, "registered", 80), (1500, "standard", 70)],
)
def test_existing_quotes(weight, service, expected):
    assert calculate_fee(weight, service) == expected


@pytest.mark.parametrize(
    "service,expected", [("standard", 60), ("registered", 80), ("express", 90)]
)
def test_service_quotes_at_1000_grams(service, expected):
    assert calculate_fee(1000, service) == expected


def test_unknown_service():
    with pytest.raises(ValueError, match="服務"):
        calculate_fee(1000, "unknown")

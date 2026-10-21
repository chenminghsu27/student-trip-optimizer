
import pytest

from data import trips, hotels
from data_validator import validate_trips, validate_hotels


def test_valid_demo_trips():
    result = validate_trips(trips)

    assert len(result) == 3
    assert result[0]["name"] == "Trip A"
    assert result[1]["name"] == "Trip B"
    assert result[2]["name"] == "Trip C"


def test_valid_demo_hotels():
    result = validate_hotels(hotels)

    assert len(result) == 3
    assert result[0]["name"] == "Budget Hostel"


def test_invalid_flight_price():
    invalid = [
        {
            "name": "Invalid Trip",
            "outbound": {
                "price": -50,
                "departure": "2026-11-10 09:00",
                "arrival": "2026-11-10 10:30",
            },
            "return": {
                "price": 75,
                "departure": "2026-11-13 19:00",
                "arrival": "2026-11-13 20:30",
            },
        }
    ]

    with pytest.raises(ValueError):
        validate_trips(invalid)


def test_invalid_flight_times():
    invalid = [
        {
            "name": "Invalid Trip",
            "outbound": {
                "price": 89,
                "departure": "2026-11-10 10:30",
                "arrival": "2026-11-10 09:00",
            },
            "return": {
                "price": 75,
                "departure": "2026-11-13 19:00",
                "arrival": "2026-11-13 20:30",
            },
        }
    ]

    with pytest.raises(ValueError):
        validate_trips(invalid)


def test_invalid_hotel_price():
    invalid = [
        {
            "name": "Invalid Hotel",
            "price_per_night": -100,
            "check_in": "15:00",
            "check_out": "10:00",
        }
    ]

    with pytest.raises(ValueError):
        validate_hotels(invalid)


def test_invalid_hotel_check_in():
    invalid = [
        {
            "name": "Invalid Hotel",
            "price_per_night": 45,
            "check_in": "invalid",
            "check_out": "10:00",
        }
    ]

    with pytest.raises(ValueError):
        validate_hotels(invalid)

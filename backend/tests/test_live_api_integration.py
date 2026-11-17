
"""Integration tests for live flight and hotel recommendations."""

from datetime import date, timedelta
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app


client = TestClient(app)

DEPARTURE_DATE = date.today() + timedelta(days=30)
RETURN_DATE = DEPARTURE_DATE + timedelta(days=3)


def make_preferences():
    """Create a valid Live Mode search request."""
    return {
        "search_mode": "live",
        "origin": "MEL",
        "destination": "SYD",
        "departure_date": DEPARTURE_DATE.isoformat(),
        "return_date": RETURN_DATE.isoformat(),
        "adults": 1,
        "max_budget": 1500,
        "earliest_departure": "07:00",
        "latest_arrival": "23:00",
        "allow_overnight_flights": False,
        "travel_style": "balanced",
    }


def make_flight(price, day, departure_time, arrival_time):
    """Create a normalized flight."""
    return {
        "price": float(price),
        "departure": f"{day} {departure_time}",
        "arrival": f"{day} {arrival_time}",
    }


def make_hotel():
    """Create a normalized Google Hotels result."""
    return {
        "name": "Test Sydney Hotel",
        "price_per_night": 100.0,
        "total_price": 300.0,
        "check_in": "15:00",
        "check_out": "10:00",
        "check_in_date": DEPARTURE_DATE.isoformat(),
        "check_out_date": RETURN_DATE.isoformat(),
        "adults": 1,
        "currency": "AUD",
    }


def mock_flight_search(origin, destination, travel_date):
    """Return different flights for outbound and return searches."""
    if origin == "MEL" and destination == "SYD":
        return [
            make_flight(
                150, travel_date, "08:00", "09:30"
            )
        ]

    if origin == "SYD" and destination == "MEL":
        return [
            make_flight(
                120, travel_date, "18:00", "19:30"
            )
        ]

    return []


@patch("api.search_hotels")
@patch("api.search_one_way_flights")
def test_live_recommendations_success(mock_flights, mock_hotels):
    """Test the complete live recommendation pipeline."""

    mock_flights.side_effect = mock_flight_search
    mock_hotels.return_value = [make_hotel()]

    response = client.post(
        "/recommendations",
        json=make_preferences(),
    )

    assert response.status_code == 200, response.text

    body = response.json()

    assert body["status"] == "success"
    assert body["meta"]["filtered_count"] >= 1
    assert body["meta"]["pareto_count"] >= 1

    assert "best_balance" in body["data"]["recommendations"]

    best = body["data"]["recommendations"]["best_balance"]

    assert best["total_price"] == 270.0
    assert best["hotel_cost"] == 300.0
    assert best["total_trip_cost"] == 570.0

    assert mock_flights.call_count == 2
    mock_hotels.assert_called_once()


@patch("api.search_hotels")
@patch("api.search_one_way_flights")
def test_live_no_flights(mock_flights, mock_hotels):
    """Reject searches with no available flights."""

    mock_flights.return_value = []
    mock_hotels.return_value = [make_hotel()]

    response = client.post(
        "/recommendations",
        json=make_preferences(),
    )

    assert response.status_code == 400
    assert "No flights found" in response.json()["detail"]


@patch("api.search_hotels")
@patch("api.search_one_way_flights")
def test_live_no_hotels(mock_flights, mock_hotels):
    """Reject searches with no hotel results."""

    mock_flights.side_effect = mock_flight_search
    mock_hotels.return_value = []

    response = client.post(
        "/recommendations",
        json=make_preferences(),
    )

    assert response.status_code == 400
    assert "No hotels found" in response.json()["detail"]


@patch("api.search_hotels")
@patch("api.search_one_way_flights")
def test_live_external_service_error(mock_flights, mock_hotels):
    """Map external search failures to HTTP 502."""

    mock_flights.side_effect = RuntimeError("API limit reached")

    response = client.post(
        "/recommendations",
        json=make_preferences(),
    )

    assert response.status_code == 502
    assert "temporarily unavailable" in response.json()["detail"]


def test_live_rejects_multiple_travellers():
    """Reject unsupported multi-traveller flight searches."""

    preferences = make_preferences()
    preferences["adults"] = 2

    response = client.post(
        "/recommendations",
        json=preferences,
    )

    assert response.status_code == 400
    assert "one traveller" in response.json()["detail"]


def test_live_rejects_past_departure_date():
    """Reject live searches for dates in the past."""

    preferences = make_preferences()
    preferences["departure_date"] = (
        date.today() - timedelta(days=2)
    ).isoformat()

    preferences["return_date"] = (
        date.today() + timedelta(days=1)
    ).isoformat()

    response = client.post(
        "/recommendations",
        json=preferences,
    )

    assert response.status_code == 400
    assert "cannot be in the past" in response.json()["detail"]

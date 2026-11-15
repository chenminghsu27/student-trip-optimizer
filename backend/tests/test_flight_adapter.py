
import pytest

from flight_adapter import adapt_flight_offer


def make_valid_offer(price=193):
    """Create a valid one-way flight offer for testing."""
    return {
        "type": "One way",
        "price": price,
        "flights": [
            {
                "departure_airport": {
                    "id": "MEL",
                    "time": "2026-11-10 08:15",
                },
                "arrival_airport": {
                    "id": "SYD",
                    "time": "2026-11-10 09:45",
                },
            }
        ],
    }


def test_adapt_one_way_flight():
    """Test converting a valid one-way flight."""
    offer = make_valid_offer()

    result = adapt_flight_offer(offer)

    assert result == {
        "price": 193.0,
        "departure": "2026-11-10 08:15",
        "arrival": "2026-11-10 09:45",
    }


def test_reject_round_trip_offer():
    """Test rejecting round-trip prices."""
    offer = make_valid_offer()
    offer["type"] = "Round trip"

    with pytest.raises(ValueError):
        adapt_flight_offer(offer)


def test_reject_empty_flights():
    """Test rejecting an offer without flight segments."""
    offer = make_valid_offer()
    offer["flights"] = []

    with pytest.raises(ValueError):
        adapt_flight_offer(offer)


@pytest.mark.parametrize(
    "price",
    [-50, "invalid", None, True, float("nan"), float("inf")],
)
def test_reject_invalid_prices(price):
    """Test rejecting invalid, negative, and non-finite prices."""
    offer = make_valid_offer(price=price)

    with pytest.raises(ValueError):
        adapt_flight_offer(offer)


def test_adapt_connecting_flight():
    """Test using the first departure and final arrival for connections."""
    offer = {
        "type": "One way",
        "price": 250,
        "flights": [
            {
                "departure_airport": {
                    "id": "MEL",
                    "time": "2026-11-10 08:00",
                },
                "arrival_airport": {
                    "id": "CBR",
                    "time": "2026-11-10 09:00",
                },
            },
            {
                "departure_airport": {
                    "id": "CBR",
                    "time": "2026-11-10 10:00",
                },
                "arrival_airport": {
                    "id": "SYD",
                    "time": "2026-11-10 12:00",
                },
            },
        ],
    }

    result = adapt_flight_offer(offer)

    assert result == {
        "price": 250.0,
        "departure": "2026-11-10 08:00",
        "arrival": "2026-11-10 12:00",
    }


@pytest.mark.parametrize(
    "departure, arrival",
    [
        ("invalid", "2026-11-10 09:45"),
        ("2026-11-10 08:15", "invalid"),
        ("2026-11-10 10:00", "2026-11-10 09:00"),
        ("2026-11-10 08:15", "2026-11-10 08:15"),
    ],
)
def test_reject_invalid_flight_times(departure, arrival):
    """Test rejecting malformed or chronologically invalid times."""
    offer = make_valid_offer()
    offer["flights"][0]["departure_airport"]["time"] = departure
    offer["flights"][0]["arrival_airport"]["time"] = arrival

    with pytest.raises(ValueError):
        adapt_flight_offer(offer)


def test_reject_missing_departure_time():
    """Test rejecting missing departure information."""
    offer = make_valid_offer()
    del offer["flights"][0]["departure_airport"]["time"]

    with pytest.raises(ValueError):
        adapt_flight_offer(offer)


def test_reject_missing_price():
    """Test rejecting an offer without a price."""
    offer = make_valid_offer()
    del offer["price"]

    with pytest.raises(ValueError):
        adapt_flight_offer(offer)


import pytest

from data import outbound_flights, return_flights, hotels
from recommendation_engine import (
    generate_flight_itineraries,
    generate_combinations,
)
from recommendation_engine import is_valid_flight_pair


# ------------------------------------------
# Test 1: Flight Combination Count
# ------------------------------------------

def test_generate_flight_itineraries_count():
    itineraries = generate_flight_itineraries(
        outbound_flights,
        return_flights
    )

    expected = len(outbound_flights) * len(return_flights)

    assert len(itineraries) == expected
    assert len(itineraries) == 144


# ------------------------------------------
# Test 2: Flight Combination Structure
# ------------------------------------------

def test_generate_flight_itineraries_structure():
    itineraries = generate_flight_itineraries(
        outbound_flights,
        return_flights
    )

    first_trip = itineraries[0]

    assert "name" in first_trip
    assert "outbound" in first_trip
    assert "return" in first_trip

    assert first_trip["outbound"] == outbound_flights[0]
    assert first_trip["return"] == return_flights[0]


# ------------------------------------------
# Test 3: Combine Flights with Hotels
# ------------------------------------------

def test_generate_full_trip_combinations():
    itineraries = generate_flight_itineraries(
        outbound_flights,
        return_flights
    )

    combinations = generate_combinations(
        itineraries,
        hotels
    )

    expected = (
        len(outbound_flights)
        * len(return_flights)
        * len(hotels)
    )

    assert len(combinations) == expected
    assert len(combinations) == 864


# ------------------------------------------
# Test 4: Empty Flight Lists
# ------------------------------------------

@pytest.mark.parametrize(
    "outbound, inbound",
    [
        ([], []),
        ([], [{"price": 80}]),
        ([{"price": 65}], []),
    ]
)
def test_generate_flight_itineraries_empty(outbound, inbound):
    itineraries = generate_flight_itineraries(
        outbound,
        inbound
    )

    assert itineraries == []
import pytest


@pytest.mark.parametrize(
    "outbound_arrival, return_departure, expected",
    [
        ("2026-11-10 10:30", "2026-11-13 19:00", True),
        ("2026-11-10 10:30", "2026-11-09 19:00", False),
        ("2026-11-10 10:30", "2026-11-10 10:30", False),
        ("2026-11-10 23:30", "2026-11-11 08:00", True),
    ]
)
def test_is_valid_flight_pair(
    outbound_arrival,
    return_departure,
    expected
):
    outbound = {
        "price": 65,
        "departure": "2026-11-10 09:00",
        "arrival": outbound_arrival
    }

    return_flight = {
        "price": 75,
        "departure": return_departure,
        "arrival": "2026-11-13 20:30"
    }

    assert is_valid_flight_pair(
        outbound,
        return_flight
    ) == expected
    def test_invalid_flight_pair_is_excluded():
        outbound_flights = [
            {
                "price": 65,
                "departure": "2026-11-10 09:00",
                "arrival": "2026-11-10 10:30"
            }
        ]

        return_flights = [
            {
                "price": 75,
                "departure": "2026-11-09 19:00",
                "arrival": "2026-11-09 20:30"
            }
        ]

        itineraries = generate_flight_itineraries(
            outbound_flights,
            return_flights
        )

        assert itineraries == []
def test_invalid_flight_pair_is_excluded():
    outbound = [{
        "price": 65,
        "departure": "2026-11-10 09:00",
        "arrival": "2026-11-10 10:30"
    }]

    inbound = [{
        "price": 75,
        "departure": "2026-11-09 19:00",
        "arrival": "2026-11-09 20:30"
    }]

    result = generate_flight_itineraries(outbound, inbound)

    assert result == []
import pytest
from calculations import calculate_flight_penalty
from calculations import calculate_total_price
from calculations import calculate_usable_hours

# ------------------------------------------
# Test Total Flight Price
#
# Verify that outbound and return
# flight prices are calculated correctly.
# ------------------------------------------

def test_calculate_total_price():

    trip = {
        "outbound": {"price": 65},
        "return": {"price": 80}
    }

    assert calculate_total_price(trip) == 145

# ------------------------------------------
# Test Flight Penalty Algorithm
#
# Verify penalties for different flight
# departure and arrival times.
# ------------------------------------------

@pytest.mark.parametrize(
    "departure, arrival, expected",
    [
        ("2026-11-10 06:00", "2026-11-10 07:30", 30),
        ("2026-11-10 07:00", "2026-11-10 08:30", 0),
        ("2026-11-10 21:59", "2026-11-10 23:30", 30),
        ("2026-11-10 22:00", "2026-11-10 23:30", 60),
        ("2026-11-10 22:30", "2026-11-11 00:00", 60),
    ]
)
def test_flight_penalty(departure, arrival, expected):

    flight = {
        "departure": departure,
        "arrival": arrival
    }

    assert calculate_flight_penalty(flight) == expected
# ------------------------------------------
# Test Usable Travel Hours
#
# Verify sightseeing hours between
# 08:00 and 22:00 each day.
# ------------------------------------------

@pytest.mark.parametrize(
    "arrival, departure, expected",
    [
        ("2026-11-10 07:30", "2026-11-13 20:00", 54.0),
        ("2026-11-10 10:30", "2026-11-13 19:00", 50.5),
        ("2026-11-11 00:00", "2026-11-13 06:00", 28.0),
        ("2026-11-10 08:00", "2026-11-10 22:00", 14.0),
        ("2026-11-10 23:00", "2026-11-11 06:00", 0.0),
    ]
)
def test_usable_hours(arrival, departure, expected):

    trip = {
        "outbound": {"arrival": arrival},
        "return": {"departure": departure}
    }

    assert calculate_usable_hours(trip) == pytest.approx(expected)
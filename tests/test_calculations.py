import pytest
from datetime import datetime
from data import TRAVEL_STYLES
from calculations import calculate_flight_penalty
from calculations import calculate_total_price
from calculations import calculate_usable_hours
from calculations import calculate_departure_penalty
from calculations import calculate_weighted_score
from calculations import dominates, find_pareto_frontier
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
# ------------------------------------------
# Test Continuous Flight Penalty
#
# Verify departure and arrival penalties
# under the updated scoring algorithm.
# ------------------------------------------

@pytest.mark.parametrize(
    "departure, arrival, expected",
    [
        ("2026-11-10 06:00", "2026-11-10 07:30", 15.0),
        ("2026-11-10 07:00", "2026-11-10 08:30", 0.0),
        ("2026-11-10 21:59", "2026-11-10 23:30", 30.0),
        ("2026-11-10 22:00", "2026-11-10 23:30", 30.0),
        ("2026-11-10 22:30", "2026-11-11 00:00", 37.5),
    ]
)
def test_flight_penalty(departure, arrival, expected):

    flight = {
        "departure": departure,
        "arrival": arrival
    }

    result = calculate_flight_penalty(flight)

    assert result == pytest.approx(expected)
# ------------------------------------------
# Test Custom Flight Penalty Rate
#
# Verify that the departure penalty
# responds to different rates.
# ------------------------------------------

@pytest.mark.parametrize(
    "rate, expected",
    [
        (5.0, 10.0),
        (15.0, 30.0),
        (30.0, 60.0),
    ]
)
def test_custom_flight_penalty(rate, expected):

    flight = {
        "departure": "2026-11-10 05:00",
        "arrival": "2026-11-10 06:30"
    }

    result = calculate_flight_penalty(
        flight,
        rate=rate
    )

    assert result == pytest.approx(expected)
# ------------------------------------------
# Test Weighted Trip Scoring
#
# Verify the relationship between
# cost, penalty, and usable hours.
# ------------------------------------------

@pytest.mark.parametrize(
    "cost, penalty, hours, time_value, expected",
    [
        (250, 30, 40, 5, 80),
        (290, 0, 55, 5, 15),
        (210, 60, 25, 5, 145),
        (250, 30, 40, 0, 280),
        (250, 30, 40, 10, -120),
    ]
)
def test_weighted_score(
    cost,
    penalty,
    hours,
    time_value,
    expected
):

    result = calculate_weighted_score(
        cost,
        penalty,
        hours,
        time_value
    )

    assert result == pytest.approx(expected)
# ------------------------------------------
# Test Invalid Weighted Score Inputs
#
# Reject negative time values and
# negative usable travel hours.
# ------------------------------------------

@pytest.mark.parametrize(
    "cost, penalty, hours, time_value",
    [
        (250, 30, 40, -5),
        (250, 30, -10, 5),
    ]
)
def test_weighted_score_invalid_input(
    cost,
    penalty,
    hours,
    time_value
):

    with pytest.raises(ValueError):
        calculate_weighted_score(
            cost,
            penalty,
            hours,
            time_value
        )
# ------------------------------------------
# Test Continuous Departure Penalty
#
# Verify proportional penalties for
# departures outside preferred hours.
# ------------------------------------------

@pytest.mark.parametrize(
    "departure, rate, expected",
    [
        ("2026-11-10 05:00", 15, 30.0),
        ("2026-11-10 06:30", 15, 7.5),
        ("2026-11-10 07:00", 15, 0.0),
        ("2026-11-10 22:00", 15, 0.0),
        ("2026-11-10 23:30", 15, 22.5),
        ("2026-11-10 05:00", 5, 10.0),
        ("2026-11-10 05:00", 30, 60.0),
    ]
)
def test_continuous_departure_penalty(
    departure,
    rate,
    expected
):

    departure_datetime = datetime.strptime(
        departure,
        "%Y-%m-%d %H:%M"
    )

    result = calculate_departure_penalty(
        departure_datetime,
        rate
    )

    assert result == pytest.approx(expected)
# ------------------------------------------
# Test Weighted Trip Ranking
#
# Verify that changing time value
# can change the recommended trip.
# ------------------------------------------

@pytest.mark.parametrize(
    "time_value, expected_trip",
    [
        (2.0, "Trip A"),
        (5.0, "Trip B"),
    ]
)
def test_weighted_trip_ranking(time_value, expected_trip):

    trips = [
        {"name": "Trip A", "cost": 200, "penalty": 0, "hours": 30},
        {"name": "Trip B", "cost": 260, "penalty": 0, "hours": 45},
    ]

    for trip in trips:
        trip["weighted_score"] = calculate_weighted_score(
            trip["cost"],
            trip["penalty"],
            trip["hours"],
            time_value
        )

    best_trip = min(
        trips,
        key=lambda trip: trip["weighted_score"]
    )

    assert best_trip["name"] == expected_trip



# ------------------------------------------
# Test Travel Style Configuration
#
# Verify that travel styles map to
# the correct time values.
# ------------------------------------------

@pytest.mark.parametrize(
    "style, expected",
    [
        ("budget", 1.0),
        ("balanced", 5.0),
        ("time-focused", 10.0),
    ]
)
def test_travel_style_configuration(style, expected):

    assert TRAVEL_STYLES[style] == expected
# ------------------------------------------
# Test Pareto Dominance
#
# Verify whether one trip dominates
# another across three objectives.
# ------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            {"total_trip_cost": 200, "usable_hours": 40, "penalty": 10},
            {"total_trip_cost": 250, "usable_hours": 35, "penalty": 20},
            True
        ),
        (
            {"total_trip_cost": 250, "usable_hours": 35, "penalty": 20},
            {"total_trip_cost": 200, "usable_hours": 40, "penalty": 10},
            False
        ),
        (
            {"total_trip_cost": 200, "usable_hours": 30, "penalty": 0},
            {"total_trip_cost": 200, "usable_hours": 35, "penalty": 30},
            False
        ),
        (
            {"total_trip_cost": 200, "usable_hours": 40, "penalty": 10},
            {"total_trip_cost": 200, "usable_hours": 40, "penalty": 10},
            False
        ),
    ]
)
def test_dominates(a, b, expected):

    assert dominates(a, b) is expected
# ------------------------------------------
# Test Pareto Frontier
#
# Verify that dominated trips are
# removed from the candidate list.
# ------------------------------------------

def test_find_pareto_frontier():

    trips = [
        {"name": "A", "total_trip_cost": 200, "usable_hours": 30, "penalty": 0},
        {"name": "B", "total_trip_cost": 250, "usable_hours": 40, "penalty": 20},
        {"name": "C", "total_trip_cost": 230, "usable_hours": 35, "penalty": 10},
        {"name": "D", "total_trip_cost": 280, "usable_hours": 38, "penalty": 0},
        {"name": "E", "total_trip_cost": 200, "usable_hours": 35, "penalty": 30},
    ]

    frontier = find_pareto_frontier(trips)

    frontier_names = {trip["name"] for trip in frontier}

    assert frontier_names == {"A", "B", "C", "D", "E"}
# ------------------------------------------
# Test Dominated Trip Removal
#
# Verify that an inferior trip
# is excluded from the frontier.
# ------------------------------------------

def test_pareto_removes_dominated_trip():

    trips = [
        {"name": "A", "total_trip_cost": 200, "usable_hours": 40, "penalty": 10},
        {"name": "B", "total_trip_cost": 250, "usable_hours": 35, "penalty": 20},
        {"name": "C", "total_trip_cost": 180, "usable_hours": 30, "penalty": 5},
    ]

    frontier = find_pareto_frontier(trips)

    frontier_names = {trip["name"] for trip in frontier}

    assert frontier_names == {"A", "C"}
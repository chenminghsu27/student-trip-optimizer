import pytest

from filters import check_preferences


# ------------------------------------------
# Test User Preference Filtering
#
# Verify that trips are accepted or
# rejected based on user preferences.
# ------------------------------------------

@pytest.mark.parametrize(
    "cost, departure, arrival, overnight, expected",
    [
        (300, "09:00", "11:00", False, True),
        (600, "09:00", "11:00", False, False),
        (300, "06:00", "11:00", False, False),
        (300, "09:00", "23:00", False, False),
        (300, "22:00", "01:00", True, True),
        (300, "22:00", "01:00", False, False),
    ]
)
def test_check_preferences(
    cost,
    departure,
    arrival,
    overnight,
    expected
):

    departure_date = "2026-11-10"

    arrival_date = (
        "2026-11-11"
        if arrival < departure
        else departure_date
    )

    trip = {
        "total_trip_cost": cost,
        "outbound": {
            "departure": f"{departure_date} {departure}",
            "arrival": f"{arrival_date} {arrival}"
        }
    }

    preferences = {
        "max_budget": 500,
        "earliest_departure": "07:00",
        "latest_arrival": "22:00",
        "allow_overnight_flights": overnight
    }

    result = check_preferences(trip, preferences)

    assert result is expected
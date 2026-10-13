import pytest

from recommendation_engine import generate_recommendations


# ------------------------------------------
# Test Complete Recommendation Pipeline
#
# Verify that flight and hotel data
# are processed correctly through
# calculations, filtering, Pareto
# optimization, and ranking.
# ------------------------------------------

def test_recommendation_pipeline():

    flights = [
        {
            "name": "Trip A",
            "outbound": {
                "price": 100,
                "departure": "2026-11-10 09:00",
                "arrival": "2026-11-10 11:00"
            },
            "return": {
                "price": 100,
                "departure": "2026-11-12 18:00",
                "arrival": "2026-11-12 20:00"
            }
        },
        {
            "name": "Trip B",
            "outbound": {
                "price": 150,
                "departure": "2026-11-10 09:00",
                "arrival": "2026-11-10 11:00"
            },
            "return": {
                "price": 150,
                "departure": "2026-11-12 18:00",
                "arrival": "2026-11-12 20:00"
            }
        }
    ]

    hotels = [
        {
            "name": "Budget Hostel",
            "price_per_night": 50,
            "check_in": "15:00",
            "check_out": "11:00"
        }
    ]

    preferences = {
        "max_budget": 500,
        "earliest_departure": "07:00",
        "latest_arrival": "22:00",
        "allow_overnight_flights": False,
        "travel_style": "balanced"
    }

    result = generate_recommendations(
        flights,
        hotels,
        preferences
    )

    assert len(result["filtered_trips"]) == 2

    assert len(result["pareto_trips"]) == 1

    assert (
        result["recommendations"]["cheapest"]["name"]
        == "Trip A + Budget Hostel"
    )

    assert (
        result["recommendations"]["best_overall"]["name"]
        == "Trip A + Budget Hostel"
    )
# ------------------------------------------
# Test No Matching Trips
#
# Verify that the recommendation
# pipeline handles empty results.
# ------------------------------------------

def test_no_matching_trips():

    flights = [
        {
            "name": "Expensive Trip",
            "outbound": {
                "price": 500,
                "departure": "2026-11-10 09:00",
                "arrival": "2026-11-10 11:00"
            },
            "return": {
                "price": 500,
                "departure": "2026-11-12 18:00",
                "arrival": "2026-11-12 20:00"
            }
        }
    ]

    hotels = [
        {
            "name": "Budget Hostel",
            "price_per_night": 50,
            "check_in": "15:00",
            "check_out": "11:00"
        }
    ]

    preferences = {
        "max_budget": 100,
        "earliest_departure": "07:00",
        "latest_arrival": "22:00",
        "allow_overnight_flights": False,
        "travel_style": "balanced"
    }

    result = generate_recommendations(
        flights,
        hotels,
        preferences
    )

    assert result["filtered_trips"] == []
    assert result["pareto_trips"] == []
    assert result["recommendations"] == {}
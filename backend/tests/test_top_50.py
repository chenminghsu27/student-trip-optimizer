from recommendation_engine import generate_recommendations
from unittest.mock import patch


def test_top_50_trips():
    # Create 60 synthetic eligible trips.
    trips = [
        {
            "name": f"Trip {i}",
            "total_trip_cost": 100 + i,
            "usable_hours": 20,
            "penalty": 0,
            "weighted_score": 100 + i,
        }
        for i in range(60)
    ]

    with (
        patch(
            "recommendation_engine.validate_preferences"
        ),
        patch(
            "recommendation_engine.validate_flight"
        ),
        patch(
            "recommendation_engine.generate_combinations",
            return_value=trips,
        ),
        patch(
            "recommendation_engine.calculate_trip_metrics",
            side_effect=lambda trip, time_value: trip,
        ),
        patch(
            "recommendation_engine.check_preferences",
            return_value=True,
        ),
        patch(
            "recommendation_engine.find_pareto_frontier",
            return_value=trips,
        ),
    ):
        result = generate_recommendations(
            flights=[],
            hotels=[],
            preferences={"value_of_time": 10},
        )

    top_50 = result["top_50_trips"]

    assert len(top_50) == 50
    assert top_50[0]["name"] == "Trip 0"
    assert top_50[-1]["name"] == "Trip 49"
    assert all(
        top_50[i]["weighted_score"]
        <= top_50[i + 1]["weighted_score"]
        for i in range(len(top_50) - 1)
    )
def test_recommendations_use_all_eligible_trips():
    trips = [
        {
            "name": f"Trip {i}",
            "total_trip_cost": 200 + i,
            "usable_hours": 20,
            "penalty": 0,
            "weighted_score": i,
        }
        for i in range(60)
    ]

    # Trip 59 is cheapest but outside the Top 50.
    trips[59]["total_trip_cost"] = 50

    # Trip 58 has the most usable hours.
    trips[58]["usable_hours"] = 100

    with (
        patch("recommendation_engine.validate_preferences"),
        patch("recommendation_engine.generate_combinations", return_value=trips),
        patch(
            "recommendation_engine.calculate_trip_metrics",
            side_effect=lambda trip, time_value: trip,
        ),
        patch("recommendation_engine.check_preferences", return_value=True),
        patch("recommendation_engine.find_pareto_frontier", return_value=trips),
    ):
        result = generate_recommendations(
            flights=[],
            hotels=[],
            preferences={"value_of_time": 10},
        )

    assert len(result["top_50_trips"]) == 50

    assert result["recommendations"]["cheapest"]["name"] == "Trip 59"
    assert result["recommendations"]["best_balance"]["name"] == "Trip 0"
    assert result["recommendations"]["most_time"]["name"] == "Trip 58"

    top_50_names = {
        trip["name"] for trip in result["top_50_trips"]
    }

    assert "Trip 59" not in top_50_names
    assert "Trip 58" not in top_50_names
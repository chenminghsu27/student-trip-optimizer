import pytest

from ranking import find_best_trip


# ------------------------------------------
# Test Best Trip Selection
#
# Verify that different metrics
# produce the correct recommendation.
# ------------------------------------------

@pytest.mark.parametrize(
    "metric, expected",
    [
        ("total_trip_cost", "Trip A"),
        ("cost_per_hour", "Trip B"),
        ("weighted_score", "Trip C"),
    ]
)
def test_find_best_trip(metric, expected):

    trips = [
        {
            "name": "Trip A",
            "total_trip_cost": 200,
            "cost_per_hour": 8,
            "weighted_score": 80
        },
        {
            "name": "Trip B",
            "total_trip_cost": 250,
            "cost_per_hour": 5,
            "weighted_score": 60
        },
        {
            "name": "Trip C",
            "total_trip_cost": 280,
            "cost_per_hour": 7,
            "weighted_score": 40
        }
    ]

    result = find_best_trip(trips, metric)

    assert result["name"] == expected


# ------------------------------------------
# Test Empty Trip List
#
# Reject ranking requests when
# no trip combinations are available.
# ------------------------------------------

def test_find_best_trip_empty():

    with pytest.raises(ValueError):
        find_best_trip([], "weighted_score")
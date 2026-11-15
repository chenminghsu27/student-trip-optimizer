
from datetime import date, timedelta

from flight_adapter import adapt_flight_offer
from recommendation_engine import (
    generate_flight_itineraries,
    generate_combinations,
    calculate_trip_metrics,
)


def make_offer(price, departure, arrival):
    """Build a SerpApi-shaped one-way flight offer."""
    return {
        "type": "One way",
        "price": price,
        "flights": [
            {
                "departure_airport": {"time": departure},
                "arrival_airport": {"time": arrival},
            }
        ],
    }


def test_flight_hotel_recommendation_integration():
    """Test flight adaptation, pairing, hotels, and scoring."""

    outbound_date = date.today() + timedelta(days=30)
    return_date = outbound_date + timedelta(days=3)

    outbound_day = outbound_date.isoformat()
    return_day = return_date.isoformat()

    outbound = [
        adapt_flight_offer(
            make_offer(
                181,
                f"{outbound_day} 06:00",
                f"{outbound_day} 07:25",
            )
        ),
        adapt_flight_offer(
            make_offer(
                215,
                f"{outbound_day} 16:45",
                f"{outbound_day} 18:10",
            )
        ),
    ]

    returns = [
        adapt_flight_offer(
            make_offer(
                128,
                f"{return_day} 06:00",
                f"{return_day} 07:35",
            )
        ),
        adapt_flight_offer(
            make_offer(
                128,
                f"{return_day} 15:15",
                f"{return_day} 16:50",
            )
        ),
    ]

    
    hotels = [
        {
            "name": "Budget Hostel",
            "price_per_night": 45.0,
            "check_in": "15:00",
            "check_out": "10:00",
        },
        {
            "name": "City Inn",
            "price_per_night": 70.0,
            "check_in": "15:00",
            "check_out": "10:00",
        },
    ]
       

    itineraries = generate_flight_itineraries(
        outbound, returns
    )

    assert len(itineraries) == 4

    combinations = generate_combinations(
        itineraries, hotels
    )

    assert len(combinations) == 8

    scored = [
        calculate_trip_metrics(trip, time_value=5.0)
        for trip in combinations
    ]

    assert len(scored) == 8

    for trip in scored:
        assert trip["total_trip_cost"] > 0
        assert trip["usable_hours"] > 0
        assert trip["weighted_score"] >= 0

    # Same outbound, return price and hotel:
    # a later return should offer more usable time.
    early_return = next(
        trip for trip in scored
        if trip["outbound"]["price"] == 181
        and trip["return"]["departure"].endswith("06:00")
        and trip["hotel"]["name"] == "Budget Hostel"
    )

    late_return = next(
        trip for trip in scored
        if trip["outbound"]["price"] == 181
        and trip["return"]["departure"].endswith("15:15")
        and trip["hotel"]["name"] == "Budget Hostel"
    )

    assert early_return["total_trip_cost"] == late_return["total_trip_cost"]
    assert late_return["usable_hours"] > early_return["usable_hours"]

from models import FlightItinerary, Hotel, Trip

from calculations import (
    calculate_total_price,
    calculate_total_penalty,
    calculate_usable_hours,
    calculate_hotel_cost,
    calculate_total_trip_cost,
    calculate_score,
    calculate_cost_per_hour,
    calculate_weighted_score,
    find_pareto_frontier,
)

from filters import check_preferences
from ranking import find_best_trip

from validation import (
    validate_flight,
    validate_hotel,
    validate_preferences,
)

from data import TRAVEL_STYLES
# ------------------------------------------
# Generate Trip Combinations
#
# Combine every flight option
# with every available hotel.
# ------------------------------------------

def generate_combinations(
    trips: list[FlightItinerary],
    hotels: list[Hotel]
) -> list[Trip]:

    combinations: list[Trip] = []

    for trip in trips:
        for hotel in hotels:

            combination: Trip = {
                "name": trip["name"] + " + " + hotel["name"],
                "outbound": trip["outbound"],
                "return": trip["return"],
                "hotel": hotel
            }

            combinations.append(combination)

    return combinations
# ------------------------------------------
# Calculate Trip Metrics
#
# Calculate all values required
# for filtering and ranking.
# ------------------------------------------

def calculate_trip_metrics(
    trip: dict,
    time_value: float
) -> dict:

    trip["total_price"] = calculate_total_price(trip)

    trip["hotel_cost"] = calculate_hotel_cost(trip)

    trip["total_trip_cost"] = calculate_total_trip_cost(trip)

    trip["penalty"] = calculate_total_penalty(trip)

    trip["usable_hours"] = calculate_usable_hours(trip)

    trip["score"] = calculate_score(trip)

    trip["cost_per_hour"] = calculate_cost_per_hour(trip)

    trip["weighted_score"] = calculate_weighted_score(
        total_cost=trip["total_trip_cost"],
        penalty=trip["penalty"],
        usable_hours=trip["usable_hours"],
        time_value=time_value
    )

    return trip
# ------------------------------------------
# Main Application
#
# Coordinate the complete trip
# recommendation workflow.
# ------------------------------------------
# ------------------------------------------
# Generate Trip Recommendations
#
# Process flight and hotel data using
# user preferences and return the
# recommended trip combinations.
# ------------------------------------------

def generate_recommendations(
    flights: list[dict],
    hotels: list[dict],
    preferences: dict
) -> dict:
        # ------------------------------------------
    # Validate Input Data
    #
    # Reject invalid data before
    # generating trip combinations.
    # ------------------------------------------

    validate_preferences(preferences)

    for trip in flights:

        for direction in ("outbound", "return"):

            if direction not in trip:
                raise ValueError(
                    f"Missing flight direction: {direction}"
                )

            validate_flight(trip[direction])

    for hotel in hotels:
        validate_hotel(hotel)
    time_value = TRAVEL_STYLES[
        preferences["travel_style"]
    ]

    # Generate combinations
    combinations = generate_combinations(
        flights,
        hotels
    )

    # Calculate metrics
    for trip in combinations:
        calculate_trip_metrics(trip, time_value)

    # Filter trips
    filtered_combinations = [
        trip
        for trip in combinations
        if check_preferences(trip, preferences)
    ]

    if not filtered_combinations:
        return {
            "filtered_trips": [],
            "pareto_trips": [],
            "recommendations": {}
        }

    # Pareto optimization
    pareto_trips = find_pareto_frontier(
        filtered_combinations
    )

    # Rank trips
    recommendations = {
        "cheapest": find_best_trip(
            filtered_combinations,
            "total_trip_cost"
        ),
        "best_time_adjusted": find_best_trip(
            filtered_combinations,
            "score"
        ),
        "best_value": find_best_trip(
            filtered_combinations,
            "cost_per_hour"
        ),
        "best_overall": find_best_trip(
            pareto_trips,
            "weighted_score"
        )
    }

    return {
        "filtered_trips": filtered_combinations,
        "pareto_trips": pareto_trips,
        "recommendations": recommendations
    }
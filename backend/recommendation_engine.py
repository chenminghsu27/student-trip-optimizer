from models import FlightItinerary, Hotel, Trip
from config import DEFAULT_VALUE_OF_TIME
from datetime import datetime
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
from validation import (
    validate_flight,
    validate_hotel,
    validate_preferences,
)
# ------------------------------------------
# Generate Trip Combinations
#
# Combine every flight option
# with every available hotel.
# ------------------------------------------
# ------------------------------------------
# Validate Flight Pair
#
# Ensure outbound arrival occurs before
# return departure.
# ------------------------------------------

def is_valid_flight_pair(
    outbound: dict,
    return_flight: dict
) -> bool:

    outbound_arrival = datetime.strptime(
        outbound["arrival"],
        "%Y-%m-%d %H:%M"
    )

    return_departure = datetime.strptime(
        return_flight["departure"],
        "%Y-%m-%d %H:%M"
    )

    return outbound_arrival < return_departure
def generate_flight_itineraries(
    outbound_flights: list[dict],
    return_flights: list[dict]
) -> list[FlightItinerary]:

    itineraries: list[FlightItinerary] = []

    for outbound_index, outbound in enumerate(
        outbound_flights, start=1
    ):
        for return_index, return_flight in enumerate(
            return_flights, start=1
        ):

            # Skip invalid flight combinations
            if not is_valid_flight_pair(
                outbound,
                return_flight
            ):
                continue

            itinerary: FlightItinerary = {
                "name": f"Trip {outbound_index}-{return_index}",
                "outbound": outbound,
                "return": return_flight
            }

            itineraries.append(itinerary)

    return itineraries
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
    custom_time_value = preferences.get("value_of_time")

    time_value = (
        DEFAULT_VALUE_OF_TIME
        if custom_time_value is None
        else custom_time_value
    )

    if not 0 < time_value <= 100:
        raise ValueError(
            "Value of time must be greater than 0 and at most 100."
        )

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
            "top_50_trips": [],
            "pareto_trips": [],
            "recommendations": {},
        }

    # Pareto optimization
    pareto_trips = find_pareto_frontier(
        filtered_combinations
    )

    # Rank trips
    # Select recommendations from all eligible trips.
    recommendations = {
        "cheapest": min(
            filtered_combinations,
            key=lambda trip: (
                trip["total_trip_cost"],
                -trip["usable_hours"],
                trip["penalty"],
            ),
        ),
        "best_balance": min(
            filtered_combinations,
            key=lambda trip: (
                trip["weighted_score"],
                trip["total_trip_cost"],
            ),
        ),
        "most_time": min(
            filtered_combinations,
            key=lambda trip: (
                -trip["usable_hours"],
                trip["total_trip_cost"],
                trip["penalty"],
            ),
        ),
    }
    # Rank all eligible trips by weighted score.
    # Lower scores represent better cost-time trade-offs.
    top_50_trips = sorted(
        filtered_combinations,
        key=lambda trip: (
            trip["weighted_score"],
            trip["total_trip_cost"],
            -trip["usable_hours"],
        ),
    )[:50]
    return {
        "filtered_trips": filtered_combinations,
        "top_50_trips": top_50_trips,
        "pareto_trips": pareto_trips,
        "recommendations": recommendations,
    }

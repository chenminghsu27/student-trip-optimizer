from datetime import datetime, timedelta
from data import trips,hotels,TRAVEL_STYLES
from ranking import find_best_trip
from filters import check_preferences
from calculations import (
    parse_datetime,
    calculate_total_price,
    calculate_total_penalty,
    calculate_usable_hours,
    calculate_hotel_nights,
    calculate_hotel_cost,
    calculate_total_trip_cost,
    calculate_score,
    calculate_cost_per_hour,
    calculate_weighted_score,
    find_pareto_frontier
)
# ------------------------------------------
# Get user travel preferences
#
# Ask the user to enter:
# - Maximum travel budget
# - Earliest departure time
# - Latest arrival time
# - Overnight flight preference
#
# Return preferences as a dictionary.
# ------------------------------------------

def get_user_preferences():

    print()
    print("================================")
    print("     STUDENT TRIP OPTIMIZER")
    print("================================")
    print()

    max_budget = get_valid_budget()

    earliest_departure = get_valid_time(
    "Earliest departure (HH:MM): "
    )

    latest_arrival = get_valid_time(
    "Latest arrival (HH:MM): "
    )

    overnight_input = input(
        "Allow overnight flights? (yes/no): "
    ).strip().lower()
    while True:

        travel_style = input(
            "Travel style (budget/balanced/time-focused): "
        ).strip().lower()

        if travel_style in TRAVEL_STYLES:
            break

        print("Invalid travel style. Please try again.")
    allow_overnight_flights = overnight_input == "yes"

    preferences = {
        "max_budget": max_budget,
        "earliest_departure": earliest_departure,
        "latest_arrival": latest_arrival,
        "allow_overnight_flights": allow_overnight_flights,
        "travel_style": travel_style
    }

    return preferences
# ------------------------------------------
# Get a valid budget from the user
#
# Keep asking until the user enters
# a valid non-negative number.
# ------------------------------------------

def get_valid_budget():

    while True:

        try:
            budget = float(
                input("Enter your maximum budget ($): ")
            )

            if budget >= 0:
                return budget

            print("Budget cannot be negative.")

        except ValueError:
            print("Invalid input. Please enter a number.")
# ------------------------------------------
# Get a valid time from the user
#
# Required format: HH:MM
#
# Example:
# 07:00
# 22:30
# ------------------------------------------

def get_valid_time(prompt):

    while True:

        user_input = input(prompt).strip()

        try:
            datetime.strptime(
                user_input,
                "%H:%M"
            )

            return user_input

        except ValueError:
            print("Invalid time. Please use HH:MM.")
# ------------------------------------------
# Generate Trip Combinations
#
# Combine every flight option
# with every available hotel.
# ------------------------------------------

def generate_combinations(trips: list[dict], hotels: list[dict]) -> list[dict]:

    combinations = []

    for trip in trips:
        for hotel in hotels:

            combination = {
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

def main():

    # ------------------------------------------
    # Get User Preferences
    # ------------------------------------------

    preferences = get_user_preferences()

    time_value = TRAVEL_STYLES[
        preferences["travel_style"]
    ]

    # ------------------------------------------
    # Generate Trip Combinations
    # ------------------------------------------

    combinations = generate_combinations(
        trips,
        hotels
    )

    # ------------------------------------------
    # Calculate Trip Metrics
    # ------------------------------------------

    for trip in combinations:
        calculate_trip_metrics(trip, time_value)

    # ------------------------------------------
    # Filter Trips
    # ------------------------------------------

    filtered_combinations = [
        trip
        for trip in combinations
        if check_preferences(trip, preferences)
    ]

    if not filtered_combinations:
        print("\nNo trips match your preferences.")
        return

    # ------------------------------------------
    # Apply Pareto Optimization
    # ------------------------------------------

    pareto_trips = find_pareto_frontier(
        filtered_combinations
    )

    # ------------------------------------------
    # Rank Trips
    # ------------------------------------------

    cheapest_trip = find_best_trip(
        filtered_combinations,
        "total_trip_cost"
    )

    best_trip = find_best_trip(
        filtered_combinations,
        "score"
    )

    best_value_trip = find_best_trip(
        filtered_combinations,
        "cost_per_hour"
    )

    best_overall_trip = find_best_trip(
        pareto_trips,
        "weighted_score"
    )

    # ------------------------------------------
    # Display Results
    # ------------------------------------------

    print("\n================================")
    print("              RESULTS")
    print("================================")

    print(
        f"Cheapest Trip: {cheapest_trip['name']} "
        f"(${cheapest_trip['total_trip_cost']:.2f})"
    )

    print(
        f"Best Time-Adjusted Trip: {best_trip['name']} "
        f"(Score: {best_trip['score']:.2f})"
    )

    print(
        f"Best Value Trip: {best_value_trip['name']} "
        f"(${best_value_trip['cost_per_hour']:.2f}/hour)"
    )

    print(
        f"Best Overall Trip: {best_overall_trip['name']} "
        f"(Score: {best_overall_trip['weighted_score']:.2f})"
    )

    print("\n================================")
    print("       PARETO OPTIMIZATION")
    print("================================")

    print(f"Filtered Trips: {len(filtered_combinations)}")
    print(f"Pareto Optimal Trips: {len(pareto_trips)}")
    print(
        "Dominated Trips Removed: "
        f"{len(filtered_combinations) - len(pareto_trips)}"
    )
if __name__ == "__main__":
    main()



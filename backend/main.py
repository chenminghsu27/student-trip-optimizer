from data import trips, hotels, TRAVEL_STYLES
from datetime import datetime
from recommendation_engine import generate_recommendations
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

def main():
    preferences = get_user_preferences()

    result = generate_recommendations(
        trips,
        hotels,
        preferences
    )

    filtered_combinations = result["filtered_trips"]

    if not filtered_combinations:
        print("\nNo trips match your preferences.")
        return

    pareto_trips = result["pareto_trips"]
    recommendations = result["recommendations"]

    cheapest_trip = recommendations["cheapest"]
    best_trip = recommendations["best_time_adjusted"]
    best_value_trip = recommendations["best_value"]
    best_overall_trip = recommendations["best_overall"]
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



from datetime import datetime, timedelta
from data import trips,hotels
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
    calculate_weighted_score
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

    allow_overnight_flights = overnight_input == "yes"

    preferences = {
        "max_budget": max_budget,
        "earliest_departure": earliest_departure,
        "latest_arrival": latest_arrival,
        "allow_overnight_flights": allow_overnight_flights
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
# Generate flight and hotel combinations
#
# Combine every flight option
# with every available hotel.
# ------------------------------------------

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


# ------------------------------------------
# Convert "22:30" → minutes
# ------------------------------------------

def time_to_minutes(time):
    parts = time.split(":")

    hour = int(parts[0])
    minute = int(parts[1])

    return hour * 60 + minute
# ------------------------------------------
# Check user preferences
#
# Return True if the trip meets all
# user requirements.
#
# Return False if any requirement fails.
# ------------------------------------------

def check_preferences(trip, preferences):

    # Check maximum budget
    if trip["total_trip_cost"] > preferences["max_budget"]:
        return False

    earliest_departure = parse_datetime(
        trip["outbound"]["departure"]
    ).time()

    latest_arrival = parse_datetime(
        trip["outbound"]["arrival"]
    ).time()

    min_departure = parse_datetime(
        "2026-01-01 " + preferences["earliest_departure"]
    ).time()

    max_arrival = parse_datetime(
        "2026-01-01 " + preferences["latest_arrival"]
    ).time()

    # Check departure time
    if earliest_departure < min_departure:
        return False

    # Check arrival time
    if latest_arrival > max_arrival:
        return False

    # Check overnight flights
    if not preferences["allow_overnight_flights"]:

        outbound_departure = parse_datetime(
            trip["outbound"]["departure"]
        )

        outbound_arrival = parse_datetime(
            trip["outbound"]["arrival"]
        )

        if outbound_arrival.date() > outbound_departure.date():
            return False

    return True
# ------------------------------------------
# Calculate everything
# ------------------------------------------
preferences = get_user_preferences()
for trip in combinations:

    # Calculate flight price
    trip["total_price"] = calculate_total_price(trip)

    # Calculate hotel cost
    trip["hotel_cost"] = calculate_hotel_cost(trip)

    # Calculate total trip cost
    trip["total_trip_cost"] = calculate_total_trip_cost(trip)

    # Calculate flight penalty
    trip["penalty"] = calculate_total_penalty(trip)

    # Calculate usable travel hours
    trip["usable_hours"] = calculate_usable_hours(trip)

    # Calculate time-adjusted score
    trip["score"] = calculate_score(trip)

    # Calculate cost per usable hour
    trip["cost_per_hour"] = calculate_cost_per_hour(trip)

    # Calculate Weighted Trip Score
    trip["weighted_score"] = calculate_weighted_score(
        total_cost=trip["total_trip_cost"],
        penalty=trip["penalty"],
        usable_hours=trip["usable_hours"],
        time_value=5.0
    )
# ------------------------------------------
# Filter combinations by user preferences
#
# Keep only trips that meet all
# user requirements.
# ------------------------------------------

filtered_combinations = []

for trip in combinations:
    if check_preferences(trip, preferences):
        filtered_combinations.append(trip)
if not filtered_combinations:
    print("\nNo trips match your preferences.")
    print("Try increasing your budget or adjusting your flight preferences.")
    raise SystemExit(0)
# ------------------------------------------
# Find cheapest trip
# ------------------------------------------

cheapest_trip = filtered_combinations[0]

for trip in filtered_combinations:
    if trip["total_trip_cost"] < cheapest_trip["total_trip_cost"]:
        cheapest_trip = trip



# ------------------------------------------
# Find best trip
# ------------------------------------------

best_trip = filtered_combinations[0]

for trip in filtered_combinations:

    if trip["score"] < best_trip["score"]:
        best_trip = trip

# ------------------------------------------
# Find best value trip
# ------------------------------------------

best_value_trip = filtered_combinations[0]

for trip in filtered_combinations:

    if trip["cost_per_hour"] < best_value_trip["cost_per_hour"]:
        best_value_trip = trip

# ------------------------------------------
# Find Best Overall Trip
#
# Select the trip with the lowest
# weighted score.
# ------------------------------------------

best_overall_trip = min(
    filtered_combinations,
    key=lambda trip: trip["weighted_score"]
)
# ------------------------------------------
# Print all trips
# ------------------------------------------

# print()
# print("================================")
# print("       STUDENT TRIP FINDER")
# print("================================")
# print()


# for trip in trips:

#     print(trip["name"])

#     print(
#         "Outbound:",
#         trip["outbound"]["departure"],
#         "→",
#         trip["outbound"]["arrival"]
#     )

#     print(
#         "Return:",
#         trip["return"]["departure"],
#         "→",
#         trip["return"]["arrival"]
#     )

#     print(
#         "Flight price: $"
#         + str(trip["total_price"])
#     )

#     print(
#         "Penalty: $"
#         + str(trip["penalty"])
#     )

#     print(
#         "Student Value Score:",
#         trip["score"]
#     )

#     print(
#         "Usable travel time:",
#         round(trip["usable_hours"], 1),
#         "hours"
#     )

#     print(
#     "Hotel:",
#     trip["hotel"]["name"]
#     )

#     print(
#         "Hotel cost: $",
#         trip["hotel_cost"]
#     )

#     print(
#         "Total trip cost: $",
#         trip["total_trip_cost"]
#     )

#     print(
#         "Cost per usable hour: $",
#         round(trip["cost_per_hour"], 2)
#     )
#     print("----------------------------")
# ------------------------------------------
# Check if any trips meet user preferences
#
# Prevent errors when no valid trips exist.
# ------------------------------------------

if not filtered_combinations:

    print("No trips match your preferences.")

    raise SystemExit

# ------------------------------------------
# Results
# ------------------------------------------

print()
print("RESULT")
print("================================")

print(
    "Cheapest trip:",
    cheapest_trip["name"],
    "- $"
    + str(cheapest_trip["total_trip_cost"])
)
print(
    "Best time-adjusted price:",
    best_trip["name"],
    "- Score:",
    best_trip["score"]
)
print(
    "Best value trip:",
    best_value_trip["name"]
)

print(
    "Cost per usable hour: $",
    round(best_value_trip["cost_per_hour"], 2)
)
# ------------------------------------------
# Display Best Overall Trip
# ------------------------------------------

print("\n================================")
print("         BEST OVERALL TRIP")
print("================================")

print(f"Trip: {best_overall_trip['name']}")
print(f"Total Cost: ${best_overall_trip['total_trip_cost']:.2f}")
print(f"Flight Penalty: ${best_overall_trip['penalty']:.2f}")
print(f"Usable Hours: {best_overall_trip['usable_hours']:.1f}")
print(f"Weighted Score: {best_overall_trip['weighted_score']:.2f}")
print()



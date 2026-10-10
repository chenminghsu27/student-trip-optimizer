from datetime import datetime
# ------------------------------------------
# Flight data
#
# Each trip contains:
# - Outbound flight
# - Return flight
# - Flight price
# - Departure and arrival datetime
# ------------------------------------------

trips = [
    {
        "name": "Trip A",

        "outbound": {
            "price": 65,
            "departure": "2026-11-10 06:00",
            "arrival": "2026-11-10 07:30"
        },

        "return": {
            "price": 80,
            "departure": "2026-11-13 20:00",
            "arrival": "2026-11-13 21:30"
        }
    },

    {
        "name": "Trip B",

        "outbound": {
            "price": 89,
            "departure": "2026-11-10 09:00",
            "arrival": "2026-11-10 10:30"
        },

        "return": {
            "price": 75,
            "departure": "2026-11-13 19:00",
            "arrival": "2026-11-13 20:30"
        }
    },

    {
        "name": "Trip C",

        "outbound": {
            "price": 55,
            "departure": "2026-11-10 22:30",
            "arrival": "2026-11-11 00:00"
        },

        "return": {
            "price": 60,
            "departure": "2026-11-13 06:00",
            "arrival": "2026-11-13 07:30"
        }
    }
]

# ------------------------------------------
# Convert string to datetime object
#
# Example:
# "2026-11-10 22:30"
# → datetime object
# ------------------------------------------

def parse_datetime(date_string):

    return datetime.strptime(
        date_string,
        "%Y-%m-%d %H:%M"
    )

# ------------------------------------------
# Convert "22:30" → minutes
# ------------------------------------------

def time_to_minutes(time):
    parts = time.split(":")

    hour = int(parts[0])
    minute = int(parts[1])

    return hour * 60 + minute


# ------------------------------------------
# Calculate penalty for one flight
#
# Early departure: Before 07:00
# Late departure: At or after 22:00
# Late arrival: At or after 23:00
# Early arrival: Before 05:00
#
# Each condition adds a $30 penalty.
# ------------------------------------------

def calculate_flight_penalty(flight):

    penalty = 0

    departure = parse_datetime(flight["departure"])
    arrival = parse_datetime(flight["arrival"])

    departure_hour = departure.hour
    arrival_hour = arrival.hour

    # Early departure
    if departure_hour < 7:
        penalty += 30

    # Late departure
    if departure_hour >= 22:
        penalty += 30

    # Late arrival
    if arrival_hour >= 23:
        penalty += 30

    # Early morning arrival
    if arrival_hour < 5:
        penalty += 30

    return penalty


# ------------------------------------------
# Calculate total ticket price
# ------------------------------------------

def calculate_total_price(trip):

    outbound_price = trip["outbound"]["price"]
    return_price = trip["return"]["price"]

    return outbound_price + return_price


# ------------------------------------------
# Calculate total penalty
# ------------------------------------------

def calculate_total_penalty(trip):

    outbound_penalty = calculate_flight_penalty(
        trip["outbound"]
    )

    return_penalty = calculate_flight_penalty(
        trip["return"]
    )

    return outbound_penalty + return_penalty


# ------------------------------------------
# Calculate usable travel hours
#
# Calculate the time between:
# - Arrival at destination
# - Departure from destination
#
# Supports different travel dates
# and overnight flights.
#
# Note:
# Sleeping time is currently included.
# ------------------------------------------

def calculate_usable_hours(trip):

    outbound_arrival = parse_datetime(
        trip["outbound"]["arrival"]
    )

    return_departure = parse_datetime(
        trip["return"]["departure"]
    )

    travel_duration = return_departure - outbound_arrival

    usable_hours = travel_duration.total_seconds() / 3600

    return max(0, usable_hours)

# ------------------------------------------
# Calculate usable hours for a single day
#
# Travel hours: 08:00 - 22:00
# Excludes overnight sleeping hours
# ------------------------------------------

def calculate_daily_usable_hours(start, end):

    travel_start = 8
    travel_end = 22

    start_hour = max(start, travel_start)
    end_hour = min(end, travel_end)

    return max(0, end_hour - start_hour)
# ------------------------------------------
# Calculate Student Value Score
#
# Lower score = better
# ------------------------------------------

def calculate_score(trip):

    price = calculate_total_price(trip)

    penalty = calculate_total_penalty(trip)

    score = price + penalty

    return score

# ------------------------------------------
# Calculate cost per usable travel hour
#
# Formula:
# Total Flight Price / Usable Travel Hours
#
# Lower cost per hour = better value
#
# If usable hours <= 0, return infinity
# to avoid division by zero.
# ------------------------------------------

def calculate_cost_per_hour(trip):

    total_price = trip["total_price"]
    usable_hours = trip["usable_hours"]

    if usable_hours <= 0:
        return float("inf")

    return total_price / usable_hours

# ------------------------------------------
# Calculate everything
# ------------------------------------------

for trip in trips:

    trip["total_price"] = calculate_total_price(trip)

    trip["penalty"] = calculate_total_penalty(trip)

    trip["usable_hours"] = calculate_usable_hours(trip)

    trip["score"] = calculate_score(trip)

    trip["cost_per_hour"] = calculate_cost_per_hour(trip)

# ------------------------------------------
# Find cheapest trip
# ------------------------------------------

cheapest_trip = trips[0]

for trip in trips:

    if trip["total_price"] < cheapest_trip["total_price"]:
        cheapest_trip = trip
# ------------------------------------------
# Find best trip
# ------------------------------------------

best_trip = trips[0]

for trip in trips:

    if trip["score"] < best_trip["score"]:
        best_trip = trip

# ------------------------------------------
# Find best value trip
# ------------------------------------------

best_value_trip = trips[0]

for trip in trips:

    if trip["cost_per_hour"] < best_value_trip["cost_per_hour"]:
        best_value_trip = trip


# ------------------------------------------
# Print all trips
# ------------------------------------------

print()
print("================================")
print("       STUDENT TRIP FINDER")
print("================================")
print()


for trip in trips:

    print(trip["name"])

    print(
        "Outbound:",
        trip["outbound"]["departure"],
        "→",
        trip["outbound"]["arrival"]
    )

    print(
        "Return:",
        trip["return"]["departure"],
        "→",
        trip["return"]["arrival"]
    )

    print(
        "Flight price: $"
        + str(trip["total_price"])
    )

    print(
        "Penalty: $"
        + str(trip["penalty"])
    )

    print(
        "Student Value Score:",
        trip["score"]
    )

    print(
        "Usable travel time:",
        round(trip["usable_hours"], 1),
        "hours"
    )

    print("----------------------------")


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
    + str(cheapest_trip["total_price"])
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
print()



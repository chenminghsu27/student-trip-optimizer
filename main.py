from datetime import datetime, timedelta
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
# Hotel data
#
# Each hotel contains:
# - Hotel name
# - Price per night
# ------------------------------------------

hotels = [
    {
        "name": "Budget Hostel",
        "price_per_night": 45
    },
    {
        "name": "City Hotel",
        "price_per_night": 80
    },
    {
        "name": "Premium Hotel",
        "price_per_night": 120
    }
]
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
# Calculate hotel cost
#
# Hotel Cost = Price Per Night × Nights
#
# Nights are calculated using:
# - Outbound arrival date
# - Return departure date
#
# Assumption:
# One hotel night per calendar night
# between arrival and return departure.
# ------------------------------------------

def calculate_hotel_cost(trip):

    arrival = parse_datetime(
        trip["outbound"]["arrival"]
    )

    departure = parse_datetime(
        trip["return"]["departure"]
    )

    nights = (departure.date() - arrival.date()).days

    nights = max(0, nights)

    price_per_night = trip["hotel"]["price_per_night"]

    return nights * price_per_night
# ------------------------------------------
# Calculate total trip cost
#
# Total Cost = Flight Price + Hotel Cost
#
# Future versions:
# - Baggage
# - Airport transport
# - Other travel expenses
# ------------------------------------------

def calculate_total_trip_cost(trip):

    flight_price = calculate_total_price(trip)

    hotel_cost = calculate_hotel_cost(trip)

    return flight_price + hotel_cost
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
# Calculate real usable travel hours
#
# Sightseeing hours: 08:00 - 22:00
#
# Only counts time between:
# - Arrival at destination
# - Departure from destination
#
# Excludes overnight sleeping hours
# Supports multiple travel days
# ------------------------------------------

def calculate_usable_hours(trip):

    outbound_arrival = parse_datetime(
        trip["outbound"]["arrival"]
    )

    return_departure = parse_datetime(
        trip["return"]["departure"]
    )

    total_usable_seconds = 0

    current_date = outbound_arrival.date()
    last_date = return_departure.date()

    while current_date <= last_date:

        day_start = datetime.combine(
            current_date,
            datetime.min.time()
        ).replace(hour=8)

        day_end = datetime.combine(
            current_date,
            datetime.min.time()
        ).replace(hour=22)

        # Find overlapping sightseeing time
        start = max(outbound_arrival, day_start)
        end = min(return_departure, day_end)

        if end > start:
            total_usable_seconds += (
                end - start
            ).total_seconds()

        current_date += timedelta(days=1)

    return total_usable_seconds / 3600


# ------------------------------------------
# Calculate Student Value Score
#
# Lower score = better
# ------------------------------------------

def calculate_score(trip):

    total_cost = trip["total_trip_cost"]
    penalty = trip["penalty"]

    return total_cost + penalty

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

    total_cost = trip["total_trip_cost"]
    usable_hours = trip["usable_hours"]

    if usable_hours <= 0:
        return float("inf")

    return total_cost / usable_hours

# ------------------------------------------
# Calculate everything
# ------------------------------------------

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

# ------------------------------------------
# Find cheapest trip
# ------------------------------------------

cheapest_trip = combinations[0]

for trip in combinations:
    if trip["total_trip_cost"] < cheapest_trip["total_trip_cost"]:
        cheapest_trip = trip
# ------------------------------------------
# Find best trip
# ------------------------------------------

best_trip = combinations[0]

for trip in combinations:

    if trip["score"] < best_trip["score"]:
        best_trip = trip

# ------------------------------------------
# Find best value trip
# ------------------------------------------

best_value_trip = combinations[0]

for trip in combinations:

    if trip["cost_per_hour"] < best_value_trip["cost_per_hour"]:
        best_value_trip = trip


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
print()



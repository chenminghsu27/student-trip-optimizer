
# ------------------------------------------
# Flight data
# ------------------------------------------

trips = [
    {
        "name": "Trip A",

        "outbound": {
            "price": 65,
            "departure": "06:00",
            "arrival": "07:30"
        },

        "return": {
            "price": 80,
            "departure": "20:00",
            "arrival": "21:30"
        }
    },

    {
        "name": "Trip B",

        "outbound": {
            "price": 89,
            "departure": "09:00",
            "arrival": "10:30"
        },

        "return": {
            "price": 75,
            "departure": "19:00",
            "arrival": "20:30"
        }
    },

    {
        "name": "Trip C",

        "outbound": {
            "price": 55,
            "departure": "22:30",
            "arrival": "00:00"
        },

        "return": {
            "price": 60,
            "departure": "06:00",
            "arrival": "07:30"
        }
    }
]


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
# ------------------------------------------

def calculate_flight_penalty(flight):

    penalty = 0

    departure = time_to_minutes(flight["departure"])
    arrival = time_to_minutes(flight["arrival"])

    # Flight leaves before 7 AM
    if departure < time_to_minutes("07:00"):
        penalty += 30

    # Flight leaves at/after 10 PM
    if departure >= time_to_minutes("22:00"):
        penalty += 30

    # Very late arrival
    if arrival >= time_to_minutes("23:00"):
        penalty += 30

    # Midnight / very early arrival
    if arrival < time_to_minutes("05:00"):
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
# Calculate usable travel time
#
# Assumption:
# The trip lasts 4 days.
#
# We measure usable time from arrival at
# destination until departure for home.
# ------------------------------------------

def calculate_usable_hours(trip):

    trip_days = 4

    arrival = time_to_minutes(
        trip["outbound"]["arrival"]
    )

    return_departure = time_to_minutes(
        trip["return"]["departure"]
    )

    # Number of minutes between:
    # arrival on day 1
    # and departure on day 4

    usable_minutes = (
        (trip_days - 1) * 24 * 60
        + return_departure
        - arrival
    )

    # If outbound arrives after midnight,
    # it actually arrives on day 2

    outbound_departure = time_to_minutes(
        trip["outbound"]["departure"]
    )

    if arrival < outbound_departure:
        usable_minutes -= 24 * 60

    return usable_minutes / 60


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
# Calculate everything
# ------------------------------------------

for trip in trips:

    trip["total_price"] = calculate_total_price(trip)

    trip["penalty"] = calculate_total_penalty(trip)

    trip["usable_hours"] = calculate_usable_hours(trip)

    trip["score"] = calculate_score(trip)


# ------------------------------------------
# Find cheapest trip
# ------------------------------------------

cheapest_trip = trips[0]

for trip in trips:

    if trip["total_price"] < cheapest_trip["total_price"]:
        cheapest_trip = trip


# ------------------------------------------
# Find best value trip
# ------------------------------------------

best_trip = trips[0]

for trip in trips:

    if trip["score"] < best_trip["score"]:
        best_trip = trip


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
    "Best value:",
    best_trip["name"],
    "- Score:",
    best_trip["score"]
)

print()


# ------------------------------------------
# Explain recommendation
# ------------------------------------------

if cheapest_trip != best_trip:

    difference = (
        best_trip["total_price"]
        - cheapest_trip["total_price"]
    )

    print(
        best_trip["name"],
        "is recommended even though it costs $"
        + str(difference),
        "more."
    )

    print(
        "It avoids inconvenient flight times."
    )
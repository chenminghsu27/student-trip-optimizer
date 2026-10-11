from datetime import datetime, timedelta
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
# Calculate total ticket price
# ------------------------------------------

def calculate_total_price(trip):

    outbound_price = trip["outbound"]["price"]
    return_price = trip["return"]["price"]

    return outbound_price + return_price
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
# Calculate hotel nights
#
# Estimate the number of hotel nights
# based on flight arrival and departure.
#
# Assumptions:
# - Early morning arrivals may require
#   an additional hotel night.
# - Travellers need accommodation
#   until their return departure date.
# ------------------------------------------

def calculate_hotel_nights(trip):

    arrival = parse_datetime(
        trip["outbound"]["arrival"]
    )

    departure = parse_datetime(
        trip["return"]["departure"]
    )

    check_in_time = parse_datetime(
        "2026-01-01 " + trip["hotel"]["check_in"]
    ).time()

    check_out_time = parse_datetime(
        "2026-01-01 " + trip["hotel"]["check_out"]
    ).time()

    # Calculate standard hotel nights
    nights = (
        departure.date() - arrival.date()
    ).days

    # Early morning arrival
    # Assume the traveller wants immediate access
    # to a hotel room.
    if arrival.time() < check_in_time:
        if arrival.hour < 6:
            nights += 1

    # Early morning return departure
    # Does not automatically require another night.
    # The last booked night already covers
    # the early departure morning.

    return max(0, nights)
# ------------------------------------------
# Calculate hotel cost
#
# Hotel Cost = Hotel Nights × Price Per Night
#
# Uses calculate_hotel_nights()
# to estimate required accommodation.
# ------------------------------------------

def calculate_hotel_cost(trip):

    nights = calculate_hotel_nights(trip)

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
from datetime import datetime

from calculations import parse_datetime


# ------------------------------------------
# Convert Time to Minutes
#
# Convert HH:MM into total minutes
# since midnight.
# ------------------------------------------

def time_to_minutes(time: str) -> int:

    hour, minute = map(int, time.split(":"))

    return hour * 60 + minute


# ------------------------------------------
# Check User Preferences
#
# Verify that a trip meets:
# - Maximum budget
# - Earliest departure
# - Latest arrival
# - Overnight flight preference
# ------------------------------------------

def check_preferences(trip: dict, preferences: dict) -> bool:

    if trip["total_trip_cost"] > preferences["max_budget"]:
        return False

    outbound_departure = parse_datetime(
        trip["outbound"]["departure"]
    )

    outbound_arrival = parse_datetime(
        trip["outbound"]["arrival"]
    )

    earliest_departure = datetime.strptime(
        preferences["earliest_departure"],
        "%H:%M"
    ).time()

    latest_arrival = datetime.strptime(
        preferences["latest_arrival"],
        "%H:%M"
    ).time()

    if outbound_departure.time() < earliest_departure:
        return False

    if outbound_arrival.time() > latest_arrival:
        return False

    if not preferences["allow_overnight_flights"]:

        if outbound_arrival.date() > outbound_departure.date():
            return False

    return True
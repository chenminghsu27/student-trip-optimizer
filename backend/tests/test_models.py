from models import (
    Flight,
    Hotel,
    Preferences
)
from typing import TypedDict
# ------------------------------------------
# Flight Itinerary Model
#
# Represent a round-trip flight option
# before accommodation is added.
# ------------------------------------------

FlightItinerary = TypedDict(
    "FlightItinerary",
    {
        "name": str,
        "outbound": Flight,
        "return": Flight
    }
)
# ------------------------------------------
# Test Flight Model Structure
#
# Verify required flight fields
# are defined correctly.
# ------------------------------------------

def test_flight_model_fields():

    assert Flight.__required_keys__ == {
        "price",
        "departure",
        "arrival"
    }


# ------------------------------------------
# Test Hotel Model Structure
#
# Verify required hotel fields
# are defined correctly.
# ------------------------------------------

def test_hotel_model_fields():

    assert Hotel.__required_keys__ == {
        "name",
        "price_per_night",
        "check_in",
        "check_out"
    }


# ------------------------------------------
# Test Preferences Model Structure
#
# Verify required preference fields
# are defined correctly.
# ------------------------------------------

def test_preferences_model_fields():

    assert Preferences.__required_keys__ == {
        "max_budget",
        "earliest_departure",
        "latest_arrival",
        "allow_overnight_flights",
        "travel_style"
    }
from typing import TypedDict


# ------------------------------------------
# Flight Data Model
#
# Define the required structure
# for a single flight.
# ------------------------------------------

class Flight(TypedDict):

    price: float
    departure: str
    arrival: str


# ------------------------------------------
# Hotel Data Model
#
# Define hotel pricing and
# check-in/check-out information.
# ------------------------------------------

class Hotel(TypedDict):

    name: str
    price_per_night: float
    check_in: str
    check_out: str


# ------------------------------------------
# Trip Data Model
#
# Combine outbound and return flights
# with accommodation information.
# ------------------------------------------

Trip = TypedDict(
    "Trip",
    {
        "name": str,
        "outbound": Flight,
        "return": Flight,
        "hotel": Hotel
    }
)
# ------------------------------------------
# Scored Trip Data Model
#
# Extend the basic trip structure
# with calculated recommendation metrics.
# ------------------------------------------

ScoredTrip = TypedDict(
    "ScoredTrip",
    {
        "name": str,
        "outbound": Flight,
        "return": Flight,
        "hotel": Hotel,

        "total_price": float,
        "hotel_cost": float,
        "total_trip_cost": float,
        "penalty": float,
        "usable_hours": float,
        "score": float,
        "cost_per_hour": float,
        "weighted_score": float
    }
)
from typing import Literal


# ------------------------------------------
# User Preferences Model
#
# Define valid user preference fields
# and supported travel styles.
# ------------------------------------------

class Preferences(TypedDict):

    max_budget: float
    earliest_departure: str
    latest_arrival: str
    allow_overnight_flights: bool

    travel_style: Literal[
        "budget",
        "balanced",
        "time-focused"
    ]
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
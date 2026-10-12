import math
from datetime import datetime
from data import TRAVEL_STYLES
# ------------------------------------------
# Validate Required Fields
#
# Ensure all required fields exist
# before processing the data.
# ------------------------------------------

def validate_required_fields(
    data: dict,
    required_fields: list[str]
) -> None:

    for field in required_fields:

        if field not in data:
            raise ValueError(
                f"Missing required field: {field}"
            )
# ------------------------------------------
# Validate Price
#
# Ensure the price is numeric,
# finite, and non-negative.
# ------------------------------------------

def validate_price(price: int | float) -> None:

    if isinstance(price, bool) or not isinstance(
        price, (int, float)
    ):
        raise ValueError("Price must be a number.")

    if not math.isfinite(price):
        raise ValueError("Price must be finite.")

    if price < 0:
        raise ValueError("Price cannot be negative.")
def validate_datetime(value: str) -> None:

    if not isinstance(value, str):
        raise ValueError("Datetime must be a string.")

    try:
        datetime.strptime(
            value,
            "%Y-%m-%d %H:%M"
        )

    except ValueError:
        raise ValueError(
            f"Invalid datetime: {value}"
        ) from None
# ------------------------------------------
# Validate Flight Data
#
# Verify required fields, price,
# datetime format, and flight duration.
# ------------------------------------------

def validate_flight(flight: dict) -> None:

    if not isinstance(flight, dict):
        raise ValueError("Flight must be a dictionary.")

    validate_required_fields(
        flight,
        ["price", "departure", "arrival"]
    )

    validate_price(flight["price"])

    validate_datetime(flight["departure"])
    validate_datetime(flight["arrival"])

    departure = datetime.strptime(
        flight["departure"],
        "%Y-%m-%d %H:%M"
    )

    arrival = datetime.strptime(
        flight["arrival"],
        "%Y-%m-%d %H:%M"
    )

    if arrival <= departure:
        raise ValueError(
            "Flight arrival must be after departure."
        )
# ------------------------------------------
# Validate Hotel Data
#
# Verify required hotel fields,
# nightly price, and check-in/out times.
# ------------------------------------------

def validate_hotel(hotel: dict) -> None:

    if not isinstance(hotel, dict):
        raise ValueError("Hotel must be a dictionary.")

    validate_required_fields(
        hotel,
        [
            "name",
            "price_per_night",
            "check_in",
            "check_out"
        ]
    )

    validate_price(hotel["price_per_night"])

    for field in ("check_in", "check_out"):

        value = hotel[field]

        if not isinstance(value, str):
            raise ValueError(
                f"Invalid hotel {field}: {value}"
            )

        try:
            datetime.strptime(value, "%H:%M")

        except ValueError:
            raise ValueError(
                f"Invalid hotel {field}: {value}"
            ) from None
# ------------------------------------------
# Validate User Preferences
#
# Verify budget, travel style,
# departure and arrival constraints.
# ------------------------------------------

def validate_preferences(preferences: dict) -> None:

    if not isinstance(preferences, dict):
        raise ValueError(
            "Preferences must be a dictionary."
        )

    validate_required_fields(
        preferences,
        [
            "max_budget",
            "earliest_departure",
            "latest_arrival",
            "allow_overnight_flights",
            "travel_style"
        ]
    )

    validate_price(preferences["max_budget"])

    if preferences["travel_style"] not in TRAVEL_STYLES:
        raise ValueError(
            "Invalid travel style."
        )

    if not isinstance(
        preferences["allow_overnight_flights"],
        bool
    ):
        raise ValueError(
            "allow_overnight_flights must be a boolean."
        )

    for field in ("earliest_departure", "latest_arrival"):

        value = preferences[field]

        if not isinstance(value, str):
            raise ValueError(
                f"Invalid preference time: {field}"
            )

        try:
            datetime.strptime(value, "%H:%M")

        except ValueError:
            raise ValueError(
                f"Invalid preference time: {field}"
            ) from None
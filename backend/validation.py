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
    """Validate demo and live hotel data."""

    if not isinstance(hotel, dict):
        raise ValueError("Hotel must be a dictionary.")

    validate_required_fields(
        hotel,
        [
            "name",
            "price_per_night",
            "check_in",
            "check_out",
        ],
    )

    if not isinstance(hotel["name"], str) or not hotel["name"].strip():
        raise ValueError("Hotel name must be a non-empty string.")

    validate_price(hotel["price_per_night"])

    for field in ("check_in", "check_out"):
        value = hotel[field]

        if not isinstance(value, str):
            raise ValueError(f"Invalid hotel {field}: {value}")

        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            raise ValueError(
                f"Invalid hotel {field}: {value}"
            ) from None

    # Live hotel pricing
    if "total_price" in hotel:
        validate_price(hotel["total_price"])

        # A live quote must identify its booking conditions.
        validate_required_fields(
            hotel,
            [
                "check_in_date",
                "check_out_date",
                "adults",
                "currency",
            ],
        )

        try:
            check_in_date = datetime.strptime(
                hotel["check_in_date"], "%Y-%m-%d"
            ).date()

            check_out_date = datetime.strptime(
                hotel["check_out_date"], "%Y-%m-%d"
            ).date()

        except (TypeError, ValueError):
            raise ValueError("Invalid hotel booking dates.") from None

        if check_out_date <= check_in_date:
            raise ValueError(
                "Hotel check-out must be after check-in."
            )

        if (
            isinstance(hotel["adults"], bool)
            or not isinstance(hotel["adults"], int)
            or hotel["adults"] < 1
        ):
            raise ValueError("Hotel adults must be a positive integer.")

        if hotel["currency"] != "AUD":
            raise ValueError("Only AUD hotel quotes are supported.")

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
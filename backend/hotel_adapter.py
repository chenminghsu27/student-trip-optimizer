
from datetime import date, datetime
from models import Hotel


def parse_hotel_time(value: str) -> str:
    """Convert Google Hotels time into HH:MM format."""

    normalized = value.replace("\u202f", " ").replace("\xa0", " ")

    return datetime.strptime(
        normalized.strip(),
        "%I:%M %p"
    ).strftime("%H:%M")


def adapt_hotel_property(
    property_data: dict,
    check_in_date: str,
    check_out_date: str,
    adults: int = 1,
    currency: str = "AUD",
) -> Hotel:
    """Convert one Google Hotels property into a Hotel."""

    start = date.fromisoformat(check_in_date)
    end = date.fromisoformat(check_out_date)

    if end <= start:
        raise ValueError(
            "Check-out date must be after check-in date."
        )

    if adults < 1:
        raise ValueError("Adults must be positive.")

    if property_data.get("type") != "hotel":
        raise ValueError("Property must be a hotel.")

    nightly = property_data.get("rate_per_night", {})
    total = property_data.get("total_rate", {})

    nightly_price = nightly.get("extracted_lowest")
    total_price = total.get("extracted_lowest")

    if nightly_price is None or total_price is None:
        raise ValueError("Hotel pricing is missing.")

    if nightly_price <= 0 or total_price <= 0:
        raise ValueError("Hotel prices must be positive.")

    hotel: Hotel = {
        "name": property_data["name"],
        "price_per_night": float(nightly_price),
        "total_price": float(total_price),
        "check_in": parse_hotel_time(
            property_data.get("check_in_time", "3:00 PM")
        ),
        "check_out": parse_hotel_time(
            property_data.get("check_out_time", "10:00 AM")
        ),
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": currency,
    }

    if "overall_rating" in property_data:
        hotel["rating"] = float(
            property_data["overall_rating"]
        )

    if "reviews" in property_data:
        hotel["reviews"] = int(
            property_data["reviews"]
        )

    if "property_token" in property_data:
        hotel["property_token"] = property_data["property_token"]

    if "link" in property_data:
        hotel["link"] = property_data["link"]

    return hotel


def adapt_hotel_results(
    response: dict,
    check_in_date: str,
    check_out_date: str,
    adults: int = 1,
    currency: str = "AUD",
) -> list[Hotel]:
    """Convert Google Hotels search results into valid hotels."""

    hotels = []

    for property_data in response.get("properties", []):
        try:
            hotel = adapt_hotel_property(
                property_data,
                check_in_date,
                check_out_date,
                adults,
                currency,
            )
        except (ValueError, KeyError, TypeError):
            continue

        hotels.append(hotel)

    return hotels

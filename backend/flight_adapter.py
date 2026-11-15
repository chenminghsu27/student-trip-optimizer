from datetime import datetime
from math import isfinite

from models import Flight


def adapt_flight_offer(offer: dict) -> Flight:
    """Convert a SerpApi one-way offer into the internal Flight format."""

    if offer.get("type") != "One way":
        raise ValueError("Expected a one-way flight offer")

    segments = offer.get("flights")

    if not isinstance(segments, list) or not segments:
        raise ValueError("Flight offer has no valid segments")

    price = offer.get("price")

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError("Invalid flight price")

    if not isfinite(price) or price < 0:
        raise ValueError("Flight price must be finite and non-negative")

    try:
        departure = segments[0]["departure_airport"]["time"]
        arrival = segments[-1]["arrival_airport"]["time"]

        departure_dt = datetime.strptime(departure, "%Y-%m-%d %H:%M")
        arrival_dt = datetime.strptime(arrival, "%Y-%m-%d %H:%M")

    except (KeyError, TypeError, ValueError, IndexError) as exc:
        raise ValueError("Invalid flight time data") from exc

    if departure_dt >= arrival_dt:
        raise ValueError("Flight arrival must be after departure")

    return {
        "price": float(price),
        "departure": departure,
        "arrival": arrival,
    }
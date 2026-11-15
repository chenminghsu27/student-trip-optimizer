
import os
from datetime import date

import requests
from dotenv import load_dotenv

from flight_adapter import adapt_flight_offer
from models import Flight


load_dotenv()


def search_one_way_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
) -> list[Flight]:
    """Search one-way Google Flights offers through SerpApi.

    Args:
        departure_id: Origin airport IATA code, e.g. MEL.
        arrival_id: Destination airport IATA code, e.g. SYD.
        outbound_date: Flight date in YYYY-MM-DD format.

    Returns:
        A list of flights in the application's internal format.

    Raises:
        ValueError: If the search parameters are invalid.
        RuntimeError: If the API key is missing or the API request fails.
    """
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY is not configured")

    if (
        len(departure_id) != 3
        or not departure_id.isalpha()
        or len(arrival_id) != 3
        or not arrival_id.isalpha()
    ):
        raise ValueError("Airport codes must contain three letters")

    departure_id = departure_id.upper()
    arrival_id = arrival_id.upper()

    if departure_id == arrival_id:
        raise ValueError("Origin and destination must be different")

    try:
        flight_date = date.fromisoformat(outbound_date)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid outbound date") from exc

    if flight_date < date.today():
        raise ValueError("Outbound date cannot be in the past")

    params = {
        "engine": "google_flights",
        "type": "2",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": "AUD",
        "gl": "au",
        "hl": "en",
        "api_key": api_key,
    }

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as exc:
        raise RuntimeError("SerpApi request failed") from exc

    if "error" in data:
        raise RuntimeError(f"SerpApi error: {data['error']}")

    offers = data.get("best_flights", []) + data.get("other_flights", [])

    flights = []

    for offer in offers:
        try:
            flights.append(adapt_flight_offer(offer))
        except (ValueError, KeyError, TypeError):
            continue

    return flights

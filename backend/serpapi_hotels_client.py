
import os
import requests

from dotenv import load_dotenv
from hotel_adapter import adapt_hotel_results

load_dotenv()

SERPAPI_URL = "https://serpapi.com/search.json"


def search_hotels(
    destination: str,
    check_in_date: str,
    check_out_date: str,
    adults: int = 1,
    max_results: int = 20,
) -> list[dict]:
    """Search Google Hotels and return normalized hotel data."""

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY is missing.")

    if not 1 <= adults <= 8:
        raise ValueError("Adults must be between 1 and 8.")

    if not 1 <= max_results <= 100:
        raise ValueError("max_results must be between 1 and 100.")

    city_names = {
        "MEL": "Melbourne",
        "SYD": "Sydney",
        "BNE": "Brisbane",
    }

    if destination not in city_names:
        raise ValueError("Unsupported hotel destination.")

    params = {
        "engine": "google_hotels",
        "q": f"Hotels in {city_names[destination]} Australia",
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": "AUD",
        "gl": "au",
        "hl": "en",
        "api_key": api_key,
    }

    response = requests.get(
        SERPAPI_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(
            f"SerpApi Google Hotels error: {data['error']}"
        )

    hotels = adapt_hotel_results(
        data,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adults=adults,
        currency="AUD",
    )

    return hotels[:max_results]

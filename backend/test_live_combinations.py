
from datetime import date, timedelta

from serpapi_client import search_one_way_flights
from recommendation_engine import generate_flight_itineraries


def main():
    departure_date = (date.today() + timedelta(days=30)).isoformat()
    return_date = (date.today() + timedelta(days=33)).isoformat()

    outbound = search_one_way_flights(
        "MEL", "SYD", departure_date
    )

    returns = search_one_way_flights(
        "SYD", "MEL", return_date
    )

    itineraries = generate_flight_itineraries(
        outbound, returns
    )

    print(f"Outbound flights: {len(outbound)}")
    print(f"Return flights: {len(returns)}")
    print(f"Valid itineraries: {len(itineraries)}")

    cheapest = sorted(
        itineraries,
        key=lambda trip: (
            trip["outbound"]["price"]
            + trip["return"]["price"]
        ),
    )

    print("\n5 cheapest flight combinations:")

    for trip in cheapest[:5]:
        total_price = (
            trip["outbound"]["price"]
            + trip["return"]["price"]
        )

        print(
            f"{trip['name']} | "
            f"A${total_price:.2f} | "
            f"Outbound: {trip['outbound']['departure']} | "
            f"Return: {trip['return']['departure']}"
        )


if __name__ == "__main__":
    main()

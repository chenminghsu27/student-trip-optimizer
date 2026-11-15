
from datetime import date, timedelta

from serpapi_client import search_one_way_flights


def main():
    # Search 30 days ahead to avoid past-date errors.
    departure_date = (date.today() + timedelta(days=30)).isoformat()
    return_date = (date.today() + timedelta(days=33)).isoformat()

    print(f"Outbound: MEL → SYD ({departure_date})")
    outbound = search_one_way_flights("MEL", "SYD", departure_date)

    print(f"Found {len(outbound)} outbound flights")
    for flight in outbound[:5]:
        print(flight)

    print(f"\nReturn: SYD → MEL ({return_date})")
    returns = search_one_way_flights("SYD", "MEL", return_date)

    print(f"Found {len(returns)} return flights")
    for flight in returns[:5]:
        print(flight)


if __name__ == "__main__":
    main()

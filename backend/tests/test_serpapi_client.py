
from datetime import date, timedelta
from unittest.mock import Mock

import pytest

from serpapi_client import search_one_way_flights


FUTURE_DATE = (date.today() + timedelta(days=30)).isoformat()


def make_offer(price, departure, arrival):
    """Create a sample SerpApi one-way flight offer."""
    return {
        "type": "One way",
        "price": price,
        "flights": [
            {
                "departure_airport": {
                    "id": "MEL",
                    "time": departure,
                },
                "arrival_airport": {
                    "id": "SYD",
                    "time": arrival,
                },
            }
        ],
    }


def test_search_one_way_flights(monkeypatch):
    """Test converting a mocked SerpApi response."""
    monkeypatch.setenv("SERPAPI_API_KEY", "test-key")

    departure = f"{FUTURE_DATE} 08:15"
    arrival = f"{FUTURE_DATE} 09:45"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "best_flights": [
            make_offer(193, departure, arrival)
        ],
        "other_flights": [
            make_offer(214, f"{FUTURE_DATE} 14:20", f"{FUTURE_DATE} 15:45")
        ],
    }

    mock_response.raise_for_status.return_value = None

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr("serpapi_client.requests.get", mock_get)

    result = search_one_way_flights("MEL", "SYD", FUTURE_DATE)

    assert len(result) == 2
    assert result[0]["price"] == 193.0
    assert result[0]["departure"] == departure
    assert result[1]["price"] == 214.0

    params = mock_get.call_args.kwargs["params"]

    assert params["type"] == "2"
    assert params["departure_id"] == "MEL"
    assert params["arrival_id"] == "SYD"
    assert params["currency"] == "AUD"


def test_missing_api_key(monkeypatch):
    """Test rejecting requests without an API key."""
    monkeypatch.delenv("SERPAPI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="not configured"):
        search_one_way_flights("MEL", "SYD", FUTURE_DATE)


@pytest.mark.parametrize(
    "origin, destination",
    [
        ("M", "SYD"),
        ("MEL", "S"),
        ("MEL", "MEL"),
        ("123", "SYD"),
    ],
)
def test_invalid_airport_codes(monkeypatch, origin, destination):
    """Test rejecting invalid airport codes."""
    monkeypatch.setenv("SERPAPI_API_KEY", "test-key")

    with pytest.raises(ValueError):
        search_one_way_flights(origin, destination, FUTURE_DATE)


def test_invalid_date(monkeypatch):
    """Test rejecting invalid flight dates."""
    monkeypatch.setenv("SERPAPI_API_KEY", "test-key")

    with pytest.raises(ValueError):
        search_one_way_flights("MEL", "SYD", "invalid-date")


def test_api_error(monkeypatch):
    """Test handling an error returned by SerpApi."""
    monkeypatch.setenv("SERPAPI_API_KEY", "test-key")

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "error": "API limit reached"
    }

    monkeypatch.setattr(
        "serpapi_client.requests.get",
        Mock(return_value=mock_response),
    )

    with pytest.raises(RuntimeError, match="API limit reached"):
        search_one_way_flights("MEL", "SYD", FUTURE_DATE)

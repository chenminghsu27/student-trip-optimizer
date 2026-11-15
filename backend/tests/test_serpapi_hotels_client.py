
from unittest.mock import Mock, patch

import pytest

from serpapi_hotels_client import search_hotels


@patch("serpapi_hotels_client.requests.get")
@patch.dict("os.environ", {"SERPAPI_API_KEY": "test-key"})
def test_search_hotels(mock_get):
    response = Mock()
    response.json.return_value = {
        "properties": [
            {
                "type": "hotel",
                "name": "Capella Sydney",
                "rate_per_night": {
                    "extracted_lowest": 892
                },
                "total_rate": {
                    "extracted_lowest": 2675
                },
                "check_in_time": "3:00 PM",
                "check_out_time": "11:00 AM",
            }
        ]
    }

    mock_get.return_value = response

    hotels = search_hotels(
        destination="SYD",
        check_in_date="2026-12-12",
        check_out_date="2026-12-15",
        adults=2,
    )

    assert len(hotels) == 1
    assert hotels[0]["name"] == "Capella Sydney"
    assert hotels[0]["total_price"] == 2675.0
    assert hotels[0]["price_per_night"] == 892.0

    params = mock_get.call_args.kwargs["params"]

    assert params["engine"] == "google_hotels"
    assert params["adults"] == 2
    assert params["currency"] == "AUD"


@pytest.mark.parametrize("destination", ["LAX", "INVALID", ""])
@patch.dict("os.environ", {"SERPAPI_API_KEY": "test-key"})
def test_unsupported_destination(destination):
    with pytest.raises(ValueError):
        search_hotels(
            destination=destination,
            check_in_date="2026-12-12",
            check_out_date="2026-12-15",
        )


@patch("serpapi_hotels_client.requests.get")
@patch.dict("os.environ", {"SERPAPI_API_KEY": "test-key"})
def test_serpapi_error(mock_get):
    response = Mock()
    response.json.return_value = {
        "error": "Invalid search parameters"
    }

    mock_get.return_value = response

    with pytest.raises(RuntimeError):
        search_hotels(
            destination="SYD",
            check_in_date="2026-12-12",
            check_out_date="2026-12-15",
        )

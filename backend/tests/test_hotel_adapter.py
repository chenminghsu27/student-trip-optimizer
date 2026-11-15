
from hotel_adapter import adapt_hotel_property


def test_adapt_google_hotel():
    property_data = {
        "type": "hotel",
        "name": "Capella Sydney",
        "check_in_time": "3:00\u202fPM",
        "check_out_time": "11:00\u202fAM",
        "rate_per_night": {
            "extracted_lowest": 892
        },
        "total_rate": {
            "extracted_lowest": 2675
        },
        "overall_rating": 4.8,
    }

    hotel = adapt_hotel_property(
        property_data,
        check_in_date="2026-12-12",
        check_out_date="2026-12-15",
        adults=2,
    )

    assert hotel["name"] == "Capella Sydney"
    assert hotel["price_per_night"] == 892.0
    assert hotel["total_price"] == 2675.0
    assert hotel["check_in"] == "15:00"
    assert hotel["check_out"] == "11:00"
    assert hotel["adults"] == 2

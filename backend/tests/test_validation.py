import pytest

from validation import (
    validate_price,
    validate_datetime,
    validate_flight,
    validate_hotel,
    validate_preferences
)
# ------------------------------------------
# Test Invalid Prices
#
# Reject negative, non-numeric,
# and non-finite prices.
# ------------------------------------------

@pytest.mark.parametrize(
    "price",
    [
        -50,
        "100",
        None,
        True,
        float("nan"),
        float("inf")
    ]
)
def test_invalid_price(price):

    with pytest.raises(ValueError):
        validate_price(price)
# ------------------------------------------
# Test Invalid Datetime
#
# Reject incorrect formats and
# impossible calendar dates.
# ------------------------------------------

@pytest.mark.parametrize(
    "value",
    [
        "2026/11/10 09:00",
        "2026-13-10 09:00",
        "2026-02-30 09:00",
        "not a date",
        None
    ]
)
def test_invalid_datetime(value):

    with pytest.raises(ValueError):
        validate_datetime(value)
# ------------------------------------------
# Test Invalid Flight Duration
#
# Reject flights where arrival
# is not after departure.
# ------------------------------------------

def test_invalid_flight_duration():

    flight = {
        "price": 100,
        "departure": "2026-11-10 12:00",
        "arrival": "2026-11-10 10:00"
    }

    with pytest.raises(ValueError):
        validate_flight(flight)
# ------------------------------------------
# Test Missing Hotel Check-in
#
# Verify that incomplete hotel
# data is rejected.
# ------------------------------------------

def test_missing_hotel_check_in():

    hotel = {
        "name": "Budget Hostel",
        "price_per_night": 50,
        "check_out": "11:00"
    }

    with pytest.raises(
        ValueError,
        match="Missing required field: check_in"
    ):
        validate_hotel(hotel)
# ------------------------------------------
# Test Invalid Travel Style
#
# Reject unsupported travel styles.
# ------------------------------------------

def test_invalid_travel_style():

    preferences = {
        "max_budget": 500,
        "earliest_departure": "07:00",
        "latest_arrival": "22:00",
        "allow_overnight_flights": False,
        "travel_style": "luxury"
    }

    with pytest.raises(
        ValueError,
        match="Invalid travel style"
    ):
        validate_preferences(preferences)
# ------------------------------------------
# Test Valid Overnight Flight
#
# Accept flights arriving on
# the following calendar day.
# ------------------------------------------

def test_valid_overnight_flight():

    flight = {
        "price": 100,
        "departure": "2026-11-10 23:00",
        "arrival": "2026-11-11 01:00"
    }

    validate_flight(flight)


# ------------------------------------------
# Test Valid Hotel Data
#
# Accept complete hotel records
# with valid check-in/out times.
# ------------------------------------------

def test_valid_hotel():

    hotel = {
        "name": "Budget Hostel",
        "price_per_night": 50,
        "check_in": "15:00",
        "check_out": "11:00"
    }

    validate_hotel(hotel)
def make_live_hotel():
    return {
        "name": "Capella Sydney",
        "price_per_night": 892.0,
        "total_price": 2675.0,
        "check_in": "15:00",
        "check_out": "11:00",
        "check_in_date": "2026-12-12",
        "check_out_date": "2026-12-15",
        "adults": 2,
        "currency": "AUD",
    }


def test_valid_live_hotel():
    validate_hotel(make_live_hotel())


@pytest.mark.parametrize(
    "price",
    [-100, "invalid", None, float("nan"), float("inf")],
)
def test_reject_invalid_total_price(price):
    hotel = make_live_hotel()
    hotel["total_price"] = price

    with pytest.raises(ValueError):
        validate_hotel(hotel)


def test_reject_invalid_hotel_dates():
    hotel = make_live_hotel()
    hotel["check_out_date"] = "2026-12-11"

    with pytest.raises(ValueError):
        validate_hotel(hotel)


def test_reject_invalid_currency():
    hotel = make_live_hotel()
    hotel["currency"] = "USD"

    with pytest.raises(ValueError):
        validate_hotel(hotel)


def test_demo_hotel_still_supported():
    hotel = {
        "name": "Budget Hostel",
        "price_per_night": 45.0,
        "check_in": "15:00",
        "check_out": "10:00",
    }

    validate_hotel(hotel)

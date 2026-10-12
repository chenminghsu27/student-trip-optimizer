import pytest

from fastapi.testclient import TestClient

from api import app


# ------------------------------------------
# Initialize API Test Client
#
# Simulate HTTP requests without
# starting a real web server.
# ------------------------------------------

client = TestClient(app)


# ------------------------------------------
# Test Health Check Endpoint
#
# Verify that the API responds
# with HTTP 200 and healthy status.
# ------------------------------------------

def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


# ------------------------------------------
# Test Valid Recommendation Request
#
# Verify that the API accepts valid
# preferences and returns results.
# ------------------------------------------

def test_valid_recommendation_request():

    payload = {
        "max_budget": 1000,
        "earliest_departure": "07:00",
        "latest_arrival": "23:59",
        "allow_overnight_flights": True,
        "travel_style": "balanced"
    }

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 200

    result = response.json()

    assert "filtered_trips" in result
    assert "pareto_trips" in result
    assert "recommendations" in result


# ------------------------------------------
# Test Invalid Budget
#
# Reject negative budget values
# with HTTP 422.
# ------------------------------------------

def test_invalid_budget():

    payload = {
        "max_budget": -100,
        "earliest_departure": "07:00",
        "latest_arrival": "23:59",
        "allow_overnight_flights": True,
        "travel_style": "balanced"
    }

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 422


# ------------------------------------------
# Test Invalid Travel Style
#
# Reject unsupported travel styles
# with HTTP 422.
# ------------------------------------------

def test_invalid_travel_style():

    payload = {
        "max_budget": 1000,
        "earliest_departure": "07:00",
        "latest_arrival": "23:59",
        "allow_overnight_flights": True,
        "travel_style": "luxury"
    }

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 422
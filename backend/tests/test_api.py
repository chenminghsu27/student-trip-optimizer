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
# Valid Demo Request Payload
# ------------------------------------------

VALID_PAYLOAD = {
    "origin": "MEL",
    "destination": "SYD",
    "departure_date": "2026-11-10",
    "return_date": "2026-11-13",
    "max_budget": 1000,
    "earliest_departure": "07:00",
    "latest_arrival": "23:59",
    "allow_overnight_flights": True,
    "travel_style": "balanced",
}


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
    payload = VALID_PAYLOAD.copy()
    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "success"
    assert "data" in result
    assert "meta" in result
    assert "recommendations" in result["data"]
    assert "pareto_trips" in result["data"] 
    assert result["meta"]["filtered_count"] >= 0
    assert result["meta"]["pareto_count"] == len(
    result["data"]["pareto_trips"]
    )


# ------------------------------------------
# Test Invalid Budget
#
# Reject negative budget values
# with HTTP 422.
# ------------------------------------------

def test_invalid_budget():

    payload = {
    **VALID_PAYLOAD,
    "max_budget": -100,
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
    **VALID_PAYLOAD,
    "travel_style": "luxury",
}

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 422
# ------------------------------------------
# Test Recommendation Validation Error
#
# Verify that engine validation errors
# are converted into HTTP 400 responses.
# ------------------------------------------

def test_recommendation_validation_error(
    monkeypatch
):

    def mock_generate_recommendations(
        flights,
        hotels,
        preferences
    ):

        raise ValueError(
            "Invalid travel preferences."
        )

    monkeypatch.setattr(
        "api.generate_recommendations",
        mock_generate_recommendations
    )

    payload = VALID_PAYLOAD.copy()

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Invalid travel preferences."
    }
# ------------------------------------------
# Test Unexpected Server Error
#
# Verify that internal exceptions
# return a safe HTTP 500 response.
# ------------------------------------------

def test_unexpected_server_error(
    monkeypatch
):

    def mock_generate_recommendations(
        flights,
        hotels,
        preferences
    ):

        raise RuntimeError(
            "Internal database connection failed."
        )

    monkeypatch.setattr(
        "api.generate_recommendations",
        mock_generate_recommendations
    )

    payload = VALID_PAYLOAD.copy()

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Internal server error."
    }
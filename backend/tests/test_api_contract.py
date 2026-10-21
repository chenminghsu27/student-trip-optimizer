import pytest

from fastapi.testclient import TestClient

from api import app


# ------------------------------------------
# Initialize API Test Client
#
# Simulate HTTP requests without
# running a real API server.
# ------------------------------------------

client = TestClient(app)


# ------------------------------------------
# Valid Test Preferences
#
# Reuse consistent request data
# across API contract tests.
# ------------------------------------------

@pytest.fixture
def valid_preferences():

    return {
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
# Test API Response Structure
#
# Verify that successful responses
# follow the expected API contract.
# ------------------------------------------

def test_response_structure(valid_preferences):

    response = client.post(
        "/recommendations",
        json=valid_preferences
    )

    assert response.status_code == 200

    result = response.json()

    assert set(result.keys()) == {
        "status",
        "data",
        "meta"
    }

    assert result["status"] == "success"

    assert set(result["data"].keys()) == {
        "recommendations",
        "pareto_trips"
    }

    assert set(result["meta"].keys()) == {
        "filtered_count",
        "pareto_count"
    }
# ------------------------------------------
# Test Metadata Consistency
#
# Verify that response metadata
# matches the actual recommendation data.
# ------------------------------------------

def test_metadata_consistency(valid_preferences):

    response = client.post(
        "/recommendations",
        json=valid_preferences
    )

    assert response.status_code == 200

    result = response.json()

    pareto_trips = result["data"]["pareto_trips"]

    assert result["meta"]["pareto_count"] == len(
        pareto_trips
    )

    assert result["meta"]["filtered_count"] >= (
        result["meta"]["pareto_count"]
    )
# ------------------------------------------
# Test Invalid Request Fields
#
# Verify that Pydantic rejects
# invalid or incomplete requests.
# ------------------------------------------

@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("max_budget", 0),
        ("max_budget", -100),
        ("earliest_departure", "25:00"),
        ("latest_arrival", "hello"),
        ("travel_style", "luxury"),
    ]
)
def test_invalid_request_fields(
    valid_preferences,
    field,
    invalid_value
):

    payload = valid_preferences.copy()

    payload[field] = invalid_value

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 422
# ------------------------------------------
# Test Missing Required Field
#
# Verify that incomplete requests
# are rejected with HTTP 422.
# ------------------------------------------

def test_missing_required_field(valid_preferences):

    payload = valid_preferences.copy()

    del payload["max_budget"]

    response = client.post(
        "/recommendations",
        json=payload
    )

    assert response.status_code == 422
# ------------------------------------------
# Test OpenAPI Documentation
#
# Verify that the API specification
# exposes the required endpoints.
# ------------------------------------------

def test_openapi_documentation():

    response = client.get("/openapi.json")

    assert response.status_code == 200

    specification = response.json()

    assert specification["info"]["title"] == (
        "Student Trip Optimizer API"
    )

    assert specification["info"]["version"] == "5.2.0"

    assert "/recommendations" in specification["paths"]

    assert "post" in specification["paths"]["/recommendations"]

    assert "/health" in specification["paths"]
# ------------------------------------------
# Test OpenAPI Response Schema
#
# Verify that the recommendation endpoint
# documents its response model.
# ------------------------------------------

def test_openapi_response_schema():

    response = client.get("/openapi.json")

    assert response.status_code == 200

    specification = response.json()

    endpoint = specification["paths"]["/recommendations"]["post"]

    success_response = endpoint["responses"]["200"]

    schema = success_response["content"]["application/json"]["schema"]

    assert schema["$ref"].endswith(
        "/RecommendationResponse"
    )
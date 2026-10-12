from fastapi import FastAPI
from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from data import trips, hotels

from recommendation_engine import generate_recommendations

# ------------------------------------------
# Initialize FastAPI Application
#
# Create the main API instance
# for Student Trip Optimizer.
# ------------------------------------------

app = FastAPI(
    title="Student Trip Optimizer API",
    description="Flight and hotel recommendation system",
    version="5.0.0"
)


# ------------------------------------------
# Root Endpoint
#
# Return basic information
# about the API.
# ------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Welcome to Student Trip Optimizer API",
        "version": "5.0.0"
    }


# ------------------------------------------
# Health Check Endpoint
#
# Verify that the API server
# is running successfully.
# ------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
# ------------------------------------------
# Trip Preferences Request Model
#
# Validate user preferences received
# through the REST API.
# ------------------------------------------

class TripPreferencesRequest(BaseModel):

    max_budget: float = Field(gt=0)

    earliest_departure: str

    latest_arrival: str

    allow_overnight_flights: bool

    travel_style: Literal[
        "budget",
        "balanced",
        "time-focused"
    ]

    @field_validator(
        "earliest_departure",
        "latest_arrival"
    )
    @classmethod
    def validate_time(cls, value: str) -> str:

        try:
            datetime.strptime(value, "%H:%M")

        except ValueError:
            raise ValueError(
                "Time must use HH:MM format."
            ) from None

        return value
# ------------------------------------------
# Generate Trip Recommendations
#
# Receive user preferences through
# an HTTP POST request and return
# recommended trip combinations.
# ------------------------------------------

@app.post("/recommendations")
def get_recommendations(
    preferences: TripPreferencesRequest
):

    result = generate_recommendations(
        trips,
        hotels,
        preferences.model_dump()
    )

    return result
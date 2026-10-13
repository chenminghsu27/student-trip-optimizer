import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from data import trips, hotels

from recommendation_engine import generate_recommendations

from fastapi import HTTPException
# ------------------------------------------
# Initialize FastAPI Application
#
# Create the main API instance
# for Student Trip Optimizer.
# ------------------------------------------

app = FastAPI(
    title="Student Trip Optimizer API",
    description=(
        "An API that helps students compare "
        "flight and accommodation options "
        "based on cost, usable travel time, "
        "and personal preferences."
    ),
    version="5.2.0",
    contact={
        "name": "Student Trip Optimizer Team"
    }
)
# ------------------------------------------
# CORS Configuration
#
# Allow the React development server
# to communicate with FastAPI.
# ------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
logger = logging.getLogger(__name__)
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
# Recommendation Data Model
#
# Define the structure of trip
# recommendation results.
# ------------------------------------------

class RecommendationData(BaseModel):

    recommendations: dict
    pareto_trips: list[dict]
# ------------------------------------------
# Response Metadata Model
#
# Provide additional information
# about the recommendation results.
# ------------------------------------------

class RecommendationMeta(BaseModel):

    filtered_count: int = Field(ge=0)
    pareto_count: int = Field(ge=0)
# ------------------------------------------
# Recommendation Response Model
#
# Define the standard API response
# for successful recommendations.
# ------------------------------------------

class RecommendationResponse(BaseModel):

    status: Literal["success"]
    data: RecommendationData
    meta: RecommendationMeta
# ------------------------------------------
# Generate Trip Recommendations
#
# Execute the recommendation engine
# and handle application errors.
# ------------------------------------------


@app.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Generate trip recommendations",
    description=(
        "Compare flight and hotel combinations "
        "using total cost, usable travel hours, "
        "flight penalties, and Pareto optimization."
    ),
    responses={
        400: {
            "description": "Invalid travel preferences"
        },
        422: {
            "description": "Request validation failed"
        },
        500: {
            "description": "Internal server error"
        }
    }
)
def get_recommendations(
    preferences: TripPreferencesRequest
):

    try:

        result = generate_recommendations(
            trips,
            hotels,
            preferences.model_dump()
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception:
        logger.exception(
            "Unexpected recommendation engine error"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        ) from None

    filtered_trips = result["filtered_trips"]
    pareto_trips = result["pareto_trips"]

    return RecommendationResponse(
        status="success",
        data=RecommendationData(
            recommendations=result["recommendations"],
            pareto_trips=pareto_trips
        ),
        meta=RecommendationMeta(
            filtered_count=len(filtered_trips),
            pareto_count=len(pareto_trips)
        )
    )

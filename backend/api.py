import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import Literal
from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator, model_validator
from data import trips, hotels
from recommendation_engine import generate_recommendations,generate_flight_itineraries
from data_validator import validate_trips, validate_hotels
from fastapi import HTTPException
from serpapi_client import search_one_way_flights
from serpapi_hotels_client import search_hotels
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
        "https://student-trip-optimizer.vercel.app",
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
    search_mode: Literal["demo", "live"] = "demo"
    adults: int = Field(default=1, ge=1, le=8)
    # V6.8 — Travel Search
    origin: Literal["MEL", "SYD", "BNE"]
    destination: Literal["MEL", "SYD", "BNE"]

    departure_date: date
    return_date: date

    # Existing preferences
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

    @model_validator(mode="after")
    def validate_search(self):

        if self.origin == self.destination:
            raise ValueError(
                "Origin and destination must be different."
            )

        if self.return_date <= self.departure_date:
            raise ValueError(
                "Return date must be after departure date."
            )

        return self

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




def get_live_trip_data(
    preferences: TripPreferencesRequest,
) -> tuple[list[dict], list[dict]]:
    """Fetch and prepare real flights and hotels."""

    if preferences.adults != 1:
        raise ValueError(
            "Live Mode currently supports one traveller only."
        )

    if preferences.departure_date < date.today():
        raise ValueError(
            "Departure date cannot be in the past."
        )

    origin = preferences.origin
    destination = preferences.destination

    departure_date = preferences.departure_date.isoformat()
    return_date = preferences.return_date.isoformat()

    # 1. Search outbound flights
    outbound_flights = search_one_way_flights(
        origin,
        destination,
        departure_date,
    )

    # 2. Search return flights
    return_flights = search_one_way_flights(
        destination,
        origin,
        return_date,
    )

    # 3. Search hotels for the same dates
    live_hotels = search_hotels(
        destination=destination,
        check_in_date=departure_date,
        check_out_date=return_date,
        adults=preferences.adults,
        max_results=20,
    )

    # 4. Validate returned data
    if not outbound_flights or not return_flights:
        raise ValueError(
            "No flights found for the selected dates."
        )

    if not live_hotels:
        raise ValueError(
            "No hotels found for the selected dates."
        )

    # 5. Limit candidate volume for MVP
    # This is a price-first shortlist, not a global optimum.
    outbound_flights = sorted(
        outbound_flights,
        key=lambda flight: flight["price"],
    )[:15]

    return_flights = sorted(
        return_flights,
        key=lambda flight: flight["price"],
    )[:15]

    live_hotels = sorted(
        live_hotels,
        key=lambda hotel: hotel["total_price"],
    )[:10]

    # 6. Generate round-trip flight itineraries
    itineraries = generate_flight_itineraries(
        outbound_flights,
        return_flights,
    )

    if not itineraries:
        raise ValueError(
            "No valid round-trip flight combinations found."
        )

    # 7. Validate the final internal data
    validated_trips = validate_trips(itineraries)
    validated_hotels = validate_hotels(live_hotels)

    return validated_trips, validated_hotels

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
    preferences: TripPreferencesRequest,
):
    """Generate recommendations using demo or live data."""

    demo_origin = "MEL"
    demo_destination = "SYD"
    demo_departure = date(2026, 11, 10)
    demo_return = date(2026, 11, 13)

    is_demo_search = (
        preferences.origin == demo_origin
        and preferences.destination == demo_destination
        and preferences.departure_date == demo_departure
        and preferences.return_date == demo_return
    )

    if preferences.search_mode == "demo" and not is_demo_search:
        raise HTTPException(
            status_code=400,
            detail=(
                "Demo Mode currently supports only "
                "MEL to SYD, 10–13 November 2026."
            ),
        )

    try:
        engine_preferences = preferences.model_dump(
            exclude={
                "search_mode",
                "adults",
                "origin",
                "destination",
                "departure_date",
                "return_date",
            }
        )

        
        if preferences.search_mode == "live":
            try:
                validated_trips, validated_hotels = (
                    get_live_trip_data(preferences)
                )
            except RuntimeError as error:
                logger.exception("External travel search failed")

                raise HTTPException(
                    status_code=502,
                    detail="Live travel search is temporarily unavailable.",
                ) from error
        else:
            validated_trips = validate_trips(trips)
            validated_hotels = validate_hotels(hotels)


        result = generate_recommendations(
            validated_trips,
            validated_hotels,
            engine_preferences,
        )
    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    

    except Exception:
        logger.exception(
            "Unexpected recommendation engine error"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from None

    filtered_trips = result["filtered_trips"]
    pareto_trips = result["pareto_trips"]

    return RecommendationResponse(
        status="success",
        data=RecommendationData(
            recommendations=result["recommendations"],
            pareto_trips=pareto_trips,
        ),
        meta=RecommendationMeta(
            filtered_count=len(filtered_trips),
            pareto_count=len(pareto_trips),
        ),
    )

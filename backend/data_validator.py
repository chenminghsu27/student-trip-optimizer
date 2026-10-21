
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class FlightData(BaseModel):
    price: float = Field(ge=0)
    departure: datetime
    arrival: datetime

    @model_validator(mode="after")
    def validate_flight_times(self):
        if self.arrival <= self.departure:
            raise ValueError(
                "Flight arrival must be after departure."
            )
        return self


class TripData(BaseModel):
    name: str = Field(min_length=1)
    outbound: FlightData
    return_flight: FlightData


class HotelData(BaseModel):
    name: str = Field(min_length=1)
    price_per_night: float = Field(ge=0)
    check_in: str
    check_out: str


def validate_trips(raw_trips):
    validated = []

    for raw in raw_trips:
        trip = TripData(
            name=raw["name"],
            outbound=raw["outbound"],
            return_flight=raw["return"],
        )

        validated.append({
            "name": trip.name,
            "outbound": {
                "price": trip.outbound.price,
                "departure": trip.outbound.departure.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "arrival": trip.outbound.arrival.strftime(
                    "%Y-%m-%d %H:%M"
                ),
            },
            "return": {
                "price": trip.return_flight.price,
                "departure": trip.return_flight.departure.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "arrival": trip.return_flight.arrival.strftime(
                    "%Y-%m-%d %H:%M"
                ),
            },
        })

    return validated


def validate_hotels(raw_hotels):
    validated = []

    for raw in raw_hotels:
        hotel = HotelData.model_validate(raw)

        # Check time format
        datetime.strptime(hotel.check_in, "%H:%M")
        datetime.strptime(hotel.check_out, "%H:%M")

        validated.append(hotel.model_dump())

    return validated


from datetime import datetime, date
from pydantic import BaseModel, Field, model_validator, ConfigDict


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
    """Validate demo hotels and live hotel quotations."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    price_per_night: float = Field(ge=0, allow_inf_nan=False)
    check_in: str
    check_out: str

    # Optional fields for Google Hotels
    total_price: float | None = Field(
        default=None,
        ge=0,
        allow_inf_nan=False,
    )
    check_in_date: date | None = None
    check_out_date: date | None = None
    adults: int | None = Field(default=None, ge=1)
    currency: str | None = None
    rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )
    reviews: int | None = Field(default=None, ge=0)
    property_token: str | None = None
    link: str | None = None

    @model_validator(mode="after")
    def validate_live_quote(self):
        if self.total_price is not None:
            if (
                self.check_in_date is None
                or self.check_out_date is None
                or self.adults is None
                or self.currency != "AUD"
            ):
                raise ValueError(
                    "Live hotel quotes require dates, "
                    "adults, and AUD currency."
                )

            if self.check_out_date <= self.check_in_date:
                raise ValueError(
                    "Hotel check-out must be after check-in."
                )

        return self



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
    """Validate hotels while preserving live quotation fields."""

    validated = []

    for raw in raw_hotels:
        hotel = HotelData.model_validate(raw)

        datetime.strptime(hotel.check_in, "%H:%M")
        datetime.strptime(hotel.check_out, "%H:%M")

        # Exclude optional fields that were not supplied.
        hotel_data = hotel.model_dump(
            mode="json",
            exclude_none=True,
        )

        validated.append(hotel_data)

    return validated

# ------------------------------------------
# Flight data
#
# Each trip contains:
# - Outbound flight
# - Return flight
# - Flight price
# - Departure and arrival datetime
# ------------------------------------------

trips = [
    {
        "name": "Trip A",

        "outbound": {
            "price": 65,
            "departure": "2026-11-10 06:00",
            "arrival": "2026-11-10 07:30"
        },

        "return": {
            "price": 80,
            "departure": "2026-11-13 20:00",
            "arrival": "2026-11-13 21:30"
        }
    },

    {
        "name": "Trip B",

        "outbound": {
            "price": 89,
            "departure": "2026-11-10 09:00",
            "arrival": "2026-11-10 10:30"
        },

        "return": {
            "price": 75,
            "departure": "2026-11-13 19:00",
            "arrival": "2026-11-13 20:30"
        }
    },

    {
        "name": "Trip C",

        "outbound": {
            "price": 55,
            "departure": "2026-11-10 22:30",
            "arrival": "2026-11-11 00:00"
        },

        "return": {
            "price": 60,
            "departure": "2026-11-13 06:00",
            "arrival": "2026-11-13 07:30"
        }
    },
    {
        "name": "Trip D",
        "outbound": {
            "price": 75,
            "departure": "2026-11-10 07:00",
            "arrival": "2026-11-10 08:30"
        },
        "return": {
            "price": 95,
            "departure": "2026-11-13 21:00",
            "arrival": "2026-11-13 22:30"
        }
    },
    {
        "name": "Trip E",
        "outbound": {
            "price": 110,
            "departure": "2026-11-10 08:00",
            "arrival": "2026-11-10 09:30"
        },
        "return": {
            "price": 65,
            "departure": "2026-11-13 18:00",
            "arrival": "2026-11-13 19:30"
        }
    },
    {
        "name": "Trip F",
        "outbound": {
            "price": 50,
            "departure": "2026-11-10 20:00",
            "arrival": "2026-11-10 21:30"
        },
        "return": {
            "price": 55,
            "departure": "2026-11-13 08:00",
            "arrival": "2026-11-13 09:30"
        }
    },
    {
        "name": "Trip G",
        "outbound": {
            "price": 130,
            "departure": "2026-11-10 06:30",
            "arrival": "2026-11-10 08:00"
        },
        "return": {
            "price": 100,
            "departure": "2026-11-13 22:00",
            "arrival": "2026-11-13 23:30"
        }
    },
    {
        "name": "Trip H",
        "outbound": {
            "price": 70,
            "departure": "2026-11-10 12:00",
            "arrival": "2026-11-10 13:30"
        },
        "return": {
            "price": 70,
            "departure": "2026-11-13 17:00",
            "arrival": "2026-11-13 18:30"
        }
    },
    {
        "name": "Trip I",
        "outbound": {
            "price": 95,
            "departure": "2026-11-10 10:00",
            "arrival": "2026-11-10 11:30"
        },
        "return": {
            "price": 85,
            "departure": "2026-11-13 20:30",
            "arrival": "2026-11-13 22:00"
        }
    },
    {
        "name": "Trip J",
        "outbound": {
            "price": 60,
            "departure": "2026-11-10 16:00",
            "arrival": "2026-11-10 17:30"
        },
        "return": {
            "price": 60,
            "departure": "2026-11-13 15:00",
            "arrival": "2026-11-13 16:30"
        }
    },
    {
        "name": "Trip K",
        "outbound": {
            "price": 140,
            "departure": "2026-11-10 05:30",
            "arrival": "2026-11-10 07:00"
        },
        "return": {
            "price": 110,
            "departure": "2026-11-13 21:30",
            "arrival": "2026-11-13 23:00"
        }
    },
    {
        "name": "Trip L",
        "outbound": {
            "price": 80,
            "departure": "2026-11-10 14:00",
            "arrival": "2026-11-10 15:30"
        },
        "return": {
            "price": 50,
            "departure": "2026-11-13 23:00",
            "arrival": "2026-11-14 00:30"
        }
    }
]
# ------------------------------------------
# Independent Flight Data
# ------------------------------------------

outbound_flights = [
    trip["outbound"]
    for trip in trips
]

return_flights = [
    trip["return"]
    for trip in trips
]
# ------------------------------------------
# Hotel data
#
# Each hotel contains:
# - Hotel name
# - Price per night
# - Check-in time
# - Check-out time
# ------------------------------------------

hotels = [
    {
        "name": "Budget Hostel",
        "price_per_night": 45,
        "check_in": "15:00",
        "check_out": "10:00"
    },
    {
        "name": "City Hotel",
        "price_per_night": 80,
        "check_in": "14:00",
        "check_out": "11:00"
    },
    {
        "name": "Premium Hotel",
        "price_per_night": 120,
        "check_in": "15:00",
        "check_out": "12:00"
    },
    {
    "name": "Capsule Hostel",
    "price_per_night": 35,
    "check_in": "15:00",
    "check_out": "10:00"
    },
    {
        "name": "Airport Hotel",
        "price_per_night": 65,
        "check_in": "14:00",
        "check_out": "10:00"
    },
    {
        "name": "Central Apartment",
        "price_per_night": 95,
        "check_in": "15:00",
        "check_out": "11:00"
    }
]  
# ------------------------------------------
# Travel Style Configuration
#
# Define the monetary value assigned
# to each usable travel hour.
# ------------------------------------------

TRAVEL_STYLES = {
    "budget": 1.0,
    "balanced": 5.0,
    "time-focused": 10.0
} 
if __name__ == "__main__":
    print("Outbound flights:", len(outbound_flights))
    print("Return flights:", len(return_flights))
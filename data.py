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
    }
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
    }
]   

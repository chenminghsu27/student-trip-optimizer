# ------------------------------------------
# Find Best Trip
#
# Select the trip with the lowest
# value for the specified metric.
# ------------------------------------------

def find_best_trip(trips: list[dict], metric: str) -> dict:

    if not trips:
        raise ValueError("Cannot rank an empty trip list.")

    return min(
        trips,
        key=lambda trip: trip[metric]
    )

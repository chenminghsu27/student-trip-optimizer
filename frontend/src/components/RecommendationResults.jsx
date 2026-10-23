import { mapRecommendationResults } from "../utils/tripMapper";
import { useState } from "react";
import RecommendationSummary from "./RecommendationSummary";
import TripList from "./TripList";

// ------------------------------------------
// Recommendation Results
//
// Sort and compare Pareto-optimal trips.
// ------------------------------------------

function RecommendationResults({ results }) {
  const [sortBy, setSortBy] = useState("recommended");

  const { trips: mappedTrips, recommendations } =
    mapRecommendationResults(results);

  const validTrips = mappedTrips.map((trip) => trip.raw);

  function getLabels(trip) {
    const mappedTrip = mappedTrips.find((item) => item.raw === trip);
    return mappedTrip?.ranking.labels ?? [];
  }

  // ------------------------------------------
  // Sort Trips
  // ------------------------------------------

  const sortedTrips = [...validTrips].sort((a, b) => {
    switch (sortBy) {
      case "price":
        return a.total_trip_cost - b.total_trip_cost;

      case "hours":
        return b.usable_hours - a.usable_hours;

      case "value":
        return a.cost_per_hour - b.cost_per_hour;

      default:
        return a.weighted_score - b.weighted_score;
    }
  });

  // ------------------------------------------
  // Compare Cheapest and Best Overall
  // ------------------------------------------

  const cheapest = recommendations.cheapest;
  const bestOverall = recommendations.best_overall;

  const differentTrips =
    cheapest &&
    bestOverall &&
    (cheapest.name !== bestOverall.name ||
      cheapest.total_trip_cost !== bestOverall.total_trip_cost);

  const extraCost = differentTrips
    ? bestOverall.total_trip_cost - cheapest.total_trip_cost
    : 0;

  const extraHours = differentTrips
    ? bestOverall.usable_hours - cheapest.usable_hours
    : 0;

  // ------------------------------------------
  // Render Results
  // ------------------------------------------

  return (
    <section className="recommendations-section">
      <div className="results-heading">
        <h2>Your Trip Recommendations</h2>

        <p>{validTrips.length} travel options based on your preferences.</p>
      </div>
      {validTrips.length === 0 ? (
        <div className="empty-results" role="status">
          <h3>No matching trips found</h3>
          <p>
            Try increasing your budget, allowing overnight flights, or adjusting
            your departure and arrival times.
          </p>
        </div>
      ) : (
        <>
          <RecommendationSummary trips={mappedTrips} />
          <div className="sorting-controls">
            <label htmlFor="sortBy">Sort By</label>

            <select
              id="sortBy"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value)}
            >
              <option value="recommended">Recommended</option>
              <option value="price">Lowest Price</option>
              <option value="hours">Most Travel Hours</option>
              <option value="value">Best Cost per Hour</option>
            </select>
          </div>
          <TripList
            trips={sortedTrips
              .map((trip) => mappedTrips.find((item) => item.raw === trip))
              .filter(Boolean)}
          />
        </>
      )}
    </section>
  );
}

export default RecommendationResults;

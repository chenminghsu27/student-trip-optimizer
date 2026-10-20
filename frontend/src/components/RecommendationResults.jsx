
import { useState } from "react";
import RecommendationCard from "./RecommendationCard";

// ------------------------------------------
// Recommendation Results
//
// Sort and compare Pareto-optimal trips.
// ------------------------------------------

function RecommendationResults({ results }) {
  const [sortBy, setSortBy] = useState("recommended");

  const recommendations =
    results?.data?.recommendations ?? {};

  const trips = results?.data?.pareto_trips ?? [];

  const categories = [
    ["best_overall", "Best Overall"],
    ["cheapest", "Cheapest"],
    ["best_value", "Best Value"],
    ["best_time_adjusted", "Best Time Adjusted"],
  ];

  // ------------------------------------------
  // Identify Recommendation Labels
  // ------------------------------------------

  function getLabels(trip) {
    return categories
      .filter(([key]) => {
        const recommended = recommendations[key];

        return (
          recommended &&
          recommended.name === trip.name &&
          recommended.total_trip_cost === trip.total_trip_cost
        );
      })
      .map(([, label]) => label);
  }

  // ------------------------------------------
  // Sort Trips
  // ------------------------------------------

  const sortedTrips = [...trips].sort((a, b) => {
    switch (sortBy) {
      case "price":
        return a.total_trip_cost - b.total_trip_cost;

      case "hours":
        return b.usable_hours - a.usable_hours;

      case "value":
        return a.cost_per_hour - b.cost_per_hour;

      default:
        return (
          a.weighted_score - b.weighted_score
        );
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
    (
      cheapest.name !== bestOverall.name ||
      cheapest.total_trip_cost !==
        bestOverall.total_trip_cost
    );

  const extraCost = differentTrips
    ? bestOverall.total_trip_cost -
      cheapest.total_trip_cost
    : 0;

  const extraHours = differentTrips
    ? bestOverall.usable_hours -
      cheapest.usable_hours
    : 0;

  // ------------------------------------------
  // Render Results
  // ------------------------------------------

  return (
    <section className="recommendations-section">
      <div className="results-heading">
        <h2>Your Trip Recommendations</h2>

        <p>
          {trips.length} Pareto-optimal travel options
          based on your preferences.
        </p>
      </div>

      {trips.length === 0 ? (
        <div className="empty-results" role="status">
        <h3>No matching trips found</h3>
        <p>
            Try increasing your budget, allowing overnight flights,
            or adjusting your departure and arrival times.
        </p>
        </div>
      ) : (
        <>
          <div className="sorting-controls">
            <label htmlFor="sortBy">Sort By</label>

            <select
              id="sortBy"
              value={sortBy}
              onChange={(event) =>
                setSortBy(event.target.value)
              }
            >
              <option value="recommended">
                Recommended
              </option>
              <option value="price">
                Lowest Price
              </option>
              <option value="hours">
                Most Travel Hours
              </option>
              <option value="value">
                Best Cost per Hour
              </option>
            </select>
          </div>

          {differentTrips && (
            <div className="comparison-summary">
              <h3>Is the cheapest trip worth it?</h3>

              <p>
                The best overall trip costs{" "}
                <strong>
                  A${Math.abs(extraCost).toFixed(2)}
                  {extraCost >= 0 ? " more" : " less"}
                </strong>
                {" "}and provides{" "}
                <strong>
                  {Math.abs(extraHours)}{" "}
                  {extraHours >= 0
                    ? "more"
                    : "fewer"}{" "}
                  usable travel hours
                </strong>
                {" "}than the cheapest option.
              </p>
            </div>
          )}

          <div className="recommendation-grid">
            {sortedTrips.map((trip, index) => (
              <RecommendationCard
                key={`${trip.name}-${trip.total_trip_cost}-${index}`}
                trip={trip}
                labels={getLabels(trip)}
              />
            ))}
          </div>
        </>
      )}
    </section>
  );
}

export default RecommendationResults;

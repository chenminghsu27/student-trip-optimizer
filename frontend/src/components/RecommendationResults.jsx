import { useState } from "react";
import { mapRecommendationResults } from "../utils/tripMapper";
import RecommendationSummary from "./RecommendationSummary";
import TripList from "./TripList";

// ------------------------------------------
// Recommendation Results
//
// Display backend-selected recommendations
// and compare the top 50 eligible trips.
// ------------------------------------------

function RecommendationResults({ results }) {
  const [sortBy, setSortBy] = useState("recommended");

  const { trips: mappedTrips, recommendations } =
    mapRecommendationResults(results);

  // ------------------------------------------
  // Sort Trips
  // ------------------------------------------

  const sortedTrips = [...mappedTrips].sort((a, b) => {
    switch (sortBy) {
      case "price":
        return a.price.total - b.price.total;

      case "hours":
        return b.travel.usableHours - a.travel.usableHours;

      case "value":
        return a.price.perHour - b.price.perHour;

      default:
        return a.ranking.weightedScore - b.ranking.weightedScore;
    }
  });

  const hasRecommendations = Object.values(recommendations).some(Boolean);

  const hasResults = mappedTrips.length > 0 || hasRecommendations;

  // ------------------------------------------
  // Render Results
  // ------------------------------------------

  return (
    <section className="recommendations-section">
      <div className="results-heading">
        <h2>Your Trip Recommendations</h2>

        <p>{mappedTrips.length} travel options available for comparison.</p>
      </div>

      {!hasResults ? (
        <div className="empty-results" role="status">
          <h3>No matching trips found</h3>
          <p>
            Try increasing your budget, allowing overnight flights, or adjusting
            your departure and arrival times.
          </p>
        </div>
      ) : (
        <>
          <RecommendationSummary recommendations={recommendations} />

          {mappedTrips.length > 0 && (
            <>
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

              <TripList trips={sortedTrips} />
            </>
          )}
        </>
      )}
    </section>
  );
}

export default RecommendationResults;

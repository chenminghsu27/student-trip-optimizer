
import RecommendationCard from "./RecommendationCard";

// ------------------------------------------
// Recommendation Results
//
// Display Pareto-optimal trips without
// duplicating recommendation categories.
// ------------------------------------------

function RecommendationResults({ results }) {
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
        <p className="empty-results">
          No matching trips found.
          Try adjusting your preferences.
        </p>
      ) : (
        <div className="recommendation-grid">
          {trips.map((trip, index) => (
            <RecommendationCard
              key={`${trip.name}-${index}`}
              trip={trip}
              labels={getLabels(trip)}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default RecommendationResults;

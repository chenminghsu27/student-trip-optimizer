import { useState } from "react";
import "./RecommendationSummary.css";
import { formatUsableHours } from "../utils/formatTime";
import { mapTrip } from "../utils/tripMapper";
import TripDetails from "./TripDetails";

const CATEGORIES = [
  {
    id: "cheapest",
    title: "Cheapest",
    explanation:
      "This trip has the lowest total cost among all eligible options.",
  },
  {
    id: "best_balance",
    title: "Best Balance",
    explanation:
      "This trip has the lowest time-adjusted score, balancing total cost, penalties, and usable travel time.",
  },
  {
    id: "most_time",
    title: "Most Time",
    explanation:
      "This trip provides the most usable travel time among all eligible options.",
  },
];

function RecommendationSummary({ recommendations = {} }) {
  const [selectedCategory, setSelectedCategory] = useState("best_balance");
  const [showExplanation, setShowExplanation] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  const availableCategories = CATEGORIES.filter(
    (category) => recommendations[category.id],
  );

  if (availableCategories.length === 0) {
    return null;
  }

  const selected =
    availableCategories.find((category) => category.id === selectedCategory) ??
    availableCategories[0];

  const trip = mapTrip(recommendations[selected.id], recommendations);

  if (!trip) {
    return null;
  }

  return (
    <section className="recommendation-summary" aria-label="Recommended trips">
      <h2>Recommended Trip</h2>

      <div
        className="recommendation-tabs"
        role="group"
        aria-label="Recommendation type"
      >
        {availableCategories.map((category) => (
          <button
            key={category.id}
            type="button"
            className={
              selected.id === category.id
                ? "recommendation-tab active"
                : "recommendation-tab"
            }
            aria-pressed={selected.id === category.id}
            onClick={() => {
              setSelectedCategory(category.id);
              setShowExplanation(false);
              setShowDetails(false);
            }}
          >
            {category.title}
          </button>
        ))}
      </div>

      <article className="recommendation-featured">
        <h3>{selected.title}</h3>

        <p className="recommendation-trip-name">{trip.name}</p>

        <div className="recommendation-metrics">
          <div>
            <span>Total Cost</span>
            <strong>A${trip.price.total.toFixed(2)}</strong>
          </div>

          <div>
            <span>Usable Time</span>
            <strong>{formatUsableHours(trip.travel.usableHours)}</strong>
          </div>
        </div>

        <button
          type="button"
          className="recommendation-explanation-toggle"
          aria-expanded={showExplanation}
          onClick={() => setShowExplanation((previous) => !previous)}
        >
          How was this selected?
        </button>

        {showExplanation && (
          <p className="recommendation-explanation">{selected.explanation}</p>
        )}
        <div className="recommendation-details-section">
          <button
            type="button"
            className="recommendation-details-toggle"
            aria-expanded={showDetails}
            onClick={() => setShowDetails((previous) => !previous)}
          >
            {showDetails ? "Hide Trip Details" : "View Trip Details"}
          </button>

          {showDetails && <TripDetails trip={trip} />}
        </div>
      </article>
    </section>
  );
}

export default RecommendationSummary;

import { useState } from "react";
import TripDetails from "./TripDetails";
import { formatUsableHours } from "../utils/formatTime";
import "./TripList.css";

function TripList({ trips = [] }) {
  const [expandedTripId, setExpandedTripId] = useState(null);

  const toggleTrip = (id) => {
    setExpandedTripId((current) => (current === id ? null : id));
  };
  const formatPrice = (value) => `A$${Number(value).toFixed(2)}`;

  if (trips.length === 0) {
    return null;
  }

  return (
    <section className="trip-list-section">
      <div className="trip-list-heading">
        <h3>Compare Trips</h3>
      </div>

      <div className="trip-list">
        {trips.map((trip, index) => (
          <article className="trip-list-item" key={`${trip.id}-${index}`}>
            <div className="trip-list-main">
              <div className="trip-list-info">
                <h3>{trip.name}</h3>
                <p className="trip-hotel-name">{trip.accommodation.name}</p>
                <div className="trip-list-labels">
                  {trip.ranking.labels.map((label) => (
                    <span className="trip-list-label" key={label}>
                      {label}
                    </span>
                  ))}
                </div>
              </div>

              <div className="trip-list-price">
                <strong>{formatPrice(trip.price.total)}</strong>
                <span>Total cost</span>
              </div>
            </div>

            <div className="trip-list-metrics">
              <div>
                <span>Usable Hours</span>
                <strong>{formatUsableHours(trip.travel.usableHours)}</strong>
              </div>

              <div>
                <span>Cost per Hour</span>
                <strong>{formatPrice(trip.price.perHour)}</strong>
              </div>
            </div>
            <button
              type="button"
              className="trip-details-toggle"
              aria-expanded={expandedTripId === trip.id}
              onClick={() => toggleTrip(trip.id)}
            >
              {expandedTripId === trip.id ? "Hide Details ▲" : "View Details ▼"}
            </button>

            {expandedTripId === trip.id && <TripDetails trip={trip} />}
          </article>
        ))}
      </div>
    </section>
  );
}

export default TripList;

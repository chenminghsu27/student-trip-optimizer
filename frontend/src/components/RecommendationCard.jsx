
import "./RecommendationCard.css";

// ------------------------------------------
// Recommendation Card
//
// Display a single recommended trip
// with price, flights, hotel, and time.
// ------------------------------------------

function RecommendationCard({ trip, labels = [] }) {
  const formatPrice = (value) =>
    `A$${Number(value).toFixed(2)}`;

  const formatDateTime = (value) =>
    value ? value.replace(" ", " • ") : "N/A";

  return (
    <article className="recommendation-card">
      <div className="card-header">
        <div className="card-labels">
          {labels.map((label) => (
            <span className="trip-label" key={label}>
              {label}
            </span>
          ))}
        </div>

        <h3>{trip.name}</h3>
        <p className="trip-total">
          {formatPrice(trip.total_trip_cost)}
        </p>
        <span className="price-caption">
          Total flight + accommodation cost
        </span>
      </div>

      <div className="trip-details">
        <div className="trip-detail">
          <strong>Outbound Flight</strong>
          <span>
            {formatDateTime(trip.outbound.departure)}
          </span>
          <span>
            Arrive: {formatDateTime(trip.outbound.arrival)}
          </span>
        </div>

        <div className="trip-detail">
          <strong>Return Flight</strong>
          <span>
            {formatDateTime(trip.return.departure)}
          </span>
          <span>
            Arrive: {formatDateTime(trip.return.arrival)}
          </span>
        </div>

        <div className="trip-detail">
          <strong>Accommodation</strong>
          <span>{trip.hotel.name}</span>
          <span>
            {formatPrice(trip.hotel.price_per_night)}
            {" / night"}
          </span>
        </div>
      </div>

      <div className="trip-metrics">
        <div>
          <span>Usable Hours</span>
          <strong>{trip.usable_hours} hrs</strong>
        </div>

        <div>
          <span>Cost per Hour</span>
          <strong>
            {formatPrice(trip.cost_per_hour)}
          </strong>
        </div>

        <div>
          <span>Flight Cost</span>
          <strong>{formatPrice(trip.total_price)}</strong>
        </div>

        <div>
          <span>Hotel Cost</span>
          <strong>{formatPrice(trip.hotel_cost)}</strong>
        </div>
      </div>

    {/* ------------------------------------------
        Recommendation Explanation
    ------------------------------------------ */}

    
    <div className="recommendation-reason">
    <strong>Why choose this trip?</strong>

    {labels.includes("Best Overall") ? (
        <p>
        This trip offers {trip.usable_hours} usable
        travel hours at approximately A$
        {trip.cost_per_hour.toFixed(2)} per hour,
        making it a strong overall choice.
        </p>
    ) : labels.includes("Cheapest") ? (
        <p>
        This option costs A$
        {trip.total_trip_cost.toFixed(2)} in total.
        Compare its {trip.usable_hours} usable hours
        with other options before choosing.
        </p>
    ) : (
        <p>
        This trip offers {trip.usable_hours} usable
        hours for A${trip.total_trip_cost.toFixed(2)}.
        </p>
    )}
    </div>



    </article>
  );
}

export default RecommendationCard;

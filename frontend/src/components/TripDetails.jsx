import { PlaneTakeoff, PlaneLanding, BedDouble } from "lucide-react";
import "./TripDetails.css";
import "./TripDetails.css";

function TripDetails({ trip }) {
  const formatPrice = (value) => `A$${Number(value).toFixed(2)}`;

  const formatDate = (value) => {
    if (!value) return "N/A";

    const [date] = value.split(" ");
    const [year, month, day] = date.split("-");

    const formatted = new Date(Number(year), Number(month) - 1, Number(day));

    return formatted.toLocaleDateString("en-AU", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const formatTime = (value) => value?.split(" ")[1]?.slice(0, 5) ?? "N/A";

  const formatDuration = (departure, arrival) => {
    if (!departure || !arrival) return "N/A";

    const start = new Date(departure.replace(" ", "T"));
    const end = new Date(arrival.replace(" ", "T"));

    const minutes = Math.round((end.getTime() - start.getTime()) / 60000);

    if (!Number.isFinite(minutes) || minutes < 0) {
      return "N/A";
    }

    const hours = Math.floor(minutes / 60);
    const remaining = minutes % 60;

    return `${hours}h ${remaining}m`;
  };

  const outbound = trip.travel.outbound;
  const inbound = trip.travel.inbound;
  const hotel = trip.accommodation;

  const flights = [
    {
      title: "Outbound Flight",
      data: outbound,
      Icon: PlaneTakeoff,
    },
    {
      title: "Return Flight",
      data: inbound,
      Icon: PlaneLanding,
    },
  ];

  return (
    <div className="expanded-trip-details">
      {flights.map(({ title, data, Icon }) => (
        <section className="trip-detail-block" key={title}>
          <h5 className="trip-detail-heading">
            <Icon size={20} strokeWidth={1.8} aria-hidden="true" />
            {title}
          </h5>
          <div className="flight-timeline">
            <div className="flight-time">
              <strong>{formatTime(data.departure)}</strong>
              <span>{formatDate(data.departure)}</span>
            </div>

            <div className="flight-duration">
              <span aria-hidden="true">→</span>
              <span>{formatDuration(data.departure, data.arrival)}</span>
            </div>

            <div className="flight-time flight-arrival">
              <strong>{formatTime(data.arrival)}</strong>
              <span>{formatDate(data.arrival)}</span>
            </div>
          </div>
        </section>
      ))}

      <section className="trip-detail-block">
        <div className="hotel-row">
          <div className="hotel-heading">
            <BedDouble size={20} strokeWidth={1.8} aria-hidden="true" />
            <div className="hotel-info">
              <h5>{hotel.name}</h5>
              <span>Accommodation</span>
            </div>
          </div>

          <div className="hotel-price">
            <strong>{formatPrice(trip.price.perNight)}</strong>
            <span>per night</span>
          </div>
        </div>
      </section>

      <section className="trip-cost-block">
        <h5>Total</h5>

        <div className="cost-row">
          <span>Flights</span>
          <strong>{formatPrice(trip.price.flights)}</strong>
        </div>

        <div className="cost-row">
          <span>Accommodation</span>
          <strong>{formatPrice(trip.price.hotel)}</strong>
        </div>

        <div className="cost-row cost-total">
          <strong>{formatPrice(trip.price.total)}</strong>
        </div>
      </section>
    </div>
  );
}

export default TripDetails;

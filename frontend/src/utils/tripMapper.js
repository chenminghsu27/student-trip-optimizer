
const CATEGORIES = [
  ["best_overall", "Best Overall"],
  ["cheapest", "Cheapest"],
  ["best_value", "Best Value"],
  ["best_time_adjusted", "Best Time Adjusted"],
];

function validNumber(value, minimum = 0) {
  return (
    typeof value === "number" &&
    Number.isFinite(value) &&
    value >= minimum
  );
}

function isValidTrip(trip) {
  return (
    trip !== null &&
    typeof trip === "object" &&
    typeof trip.name === "string" &&
    validNumber(trip.total_trip_cost) &&
    validNumber(trip.total_price) &&
    validNumber(trip.hotel_cost) &&
    validNumber(trip.usable_hours, 0.000001) &&
    validNumber(trip.cost_per_hour) &&
    Number.isFinite(trip.weighted_score) &&
    typeof trip.outbound?.departure === "string" &&
    typeof trip.outbound?.arrival === "string" &&
    typeof trip.return?.departure === "string" &&
    typeof trip.return?.arrival === "string" &&
    typeof trip.hotel?.name === "string" &&
    validNumber(trip.hotel?.price_per_night)
  );
}

function matchesRecommendation(trip, recommendation) {
  return (
    recommendation &&
    recommendation.name === trip.name &&
    recommendation.total_trip_cost === trip.total_trip_cost
  );
}

export function mapTrip(trip, recommendations = {}) {
  if (!isValidTrip(trip)) {
    return null;
  }

  const labels = CATEGORIES
    .filter(([key]) =>
      matchesRecommendation(trip, recommendations[key])
    )
    .map(([, label]) => label);

  return {
    // Temporary ID until backend provides stable IDs
    id: [
      trip.name,
      trip.outbound.departure,
      trip.outbound.arrival,
      trip.return.departure,
      trip.return.arrival,
      trip.hotel.name,
    ].join("|"),

    name: trip.name,

    price: {
      total: trip.total_trip_cost,
      flights: trip.total_price,
      hotel: trip.hotel_cost,
      perHour: trip.cost_per_hour,
      perNight: trip.hotel.price_per_night,
    },

    travel: {
      usableHours: trip.usable_hours,
      outbound: { ...trip.outbound },
      inbound: { ...trip.return },
    },

    accommodation: {
      ...trip.hotel,
    },

    ranking: {
      weightedScore: trip.weighted_score,
      labels,
    },

    // Keep original data for compatibility during migration
    raw: trip,
  };
}

export function mapRecommendationResults(results) {
  const recommendations =
    results?.data?.recommendations ?? {};

  const trips = Array.isArray(results?.data?.pareto_trips)
    ? results.data.pareto_trips
    : [];

  const mappedTrips = trips
    .map((trip) => mapTrip(trip, recommendations))
    .filter(Boolean);

  return {
    trips: mappedTrips,
    recommendations,
    count: mappedTrips.length,
  };
}

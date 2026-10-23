import "./RecommendationSummary.css";

function RecommendationSummary({ trips }) {
  if (!trips || trips.length === 0) {
    return null;
  }

  // Cheapest: lowest total trip cost
  const cheapest = [...trips].sort((a, b) => a.price.total - b.price.total)[0];

  // Best Overall: lowest weighted score
  const bestOverall = [...trips].sort(
    (a, b) => a.ranking.weightedScore - b.ranking.weightedScore,
  )[0];

  // Most Time: highest usable travel hours
  const mostTime = [...trips].sort(
    (a, b) => b.travel.usableHours - a.travel.usableHours,
  )[0];

  const summaryItems = [
    {
      id: "cheapest",
      title: "Cheapest",
      value: `A$${cheapest.price.total.toFixed(2)}`,
      description: "Lowest total cost",
      trip: cheapest,
    },
    {
      id: "overall",
      title: "Best Overall",
      value: `A$${bestOverall.price.total.toFixed(2)}`,
      description: `${bestOverall.travel.usableHours} usable hours`,
      trip: bestOverall,
    },
    {
      id: "time",
      title: "Most Time",
      value: `${mostTime.travel.usableHours}h`,
      description: "Longest usable travel time",
      trip: mostTime,
    },
  ];

  return (
    <section
      className="recommendation-summary"
      aria-labelledby="summary-heading"
    >
      <div className="summary-grid">
        {summaryItems.map((item) => (
          <article className="summary-card" key={item.id}>
            <span className={`summary-type ${item.id}`}>{item.title}</span>

            <strong className="summary-value">{item.value}</strong>

            <span className="summary-description">{item.description}</span>

            <span className="summary-trip-name">{item.trip.name}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

export default RecommendationSummary;

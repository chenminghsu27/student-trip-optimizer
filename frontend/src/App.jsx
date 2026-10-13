import { useState } from "react";
import "./App.css";

// ------------------------------------------
// Student Trip Optimizer
//
// V6.1 - Travel Preferences Form
//
// Allow users to enter their travel
// preferences before searching for trips.
// ------------------------------------------

function App() {

  // ------------------------------------------
  // Application State
  // ------------------------------------------

  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState(null);
  const [preferences, setPreferences] = useState({
    max_budget: 500,
    earliest_departure: "07:00",
    latest_arrival: "23:00",
    allow_overnight_flights: false,
    travel_style: "balanced",
  });

  // ------------------------------------------
  // Handle Input Changes
  // ------------------------------------------

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setPreferences((previous) => ({
      ...previous,
      [name]:
        type === "checkbox"
          ? checked
          : type === "number"
            ? (value === "" ? "" : Number(value))
            : value,
    }));
  }

  // ------------------------------------------
  // Handle Form Submission
  // ------------------------------------------

  // ------------------------------------------
// Handle Form Submission
//
// Send travel preferences to FastAPI
// and receive recommendations.
// ------------------------------------------

  async function handleSubmit(event) {
    event.preventDefault();

    if (
      preferences.max_budget === "" ||
      !Number.isFinite(preferences.max_budget) ||
      preferences.max_budget <= 0
    ) {
      setError("Please enter a valid budget.");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await fetch(
        "http://localhost:8000/recommendations",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(preferences),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        const detail = result.detail;

        throw new Error(
          typeof detail === "string"
            ? detail
            : `Request failed (${response.status})`
        );
      }

      setResults(result);

      console.log("API Response:", result);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "An unexpected error occurred."
      );

    } finally {
      setLoading(false);
    }
  }

  // ------------------------------------------
  // Render Application
  // ------------------------------------------

  return (
    <div className="app">

      <header className="navbar">
        <h2>✈ Student Trip Optimizer</h2>
      </header>

      <main className="hero">

        {!showForm ? (

          <div className="hero-content">

            <span className="badge">
              Travel Smarter, Spend Less
            </span>

            <h1>Find Your Perfect Trip</h1>

            <p>
              Compare flights and accommodation
              based on your budget, travel time,
              and personal preferences.
            </p>

            <button
              className="start-button"
              onClick={() => setShowForm(true)}
            >
              Get Started
            </button>

          </div>

        ) : (

          <div className="form-container">

            <h1>Travel Preferences</h1>

            <p>
              Tell us what matters most to you.
            </p>

            <form onSubmit={handleSubmit}>

              <div className="form-group">
                <label htmlFor="max_budget">
                  Maximum Budget (AUD)
                </label>

                <input
                  id="max_budget"
                  type="number"
                  name="max_budget"
                  min="1"
                  required
                  value={preferences.max_budget}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="earliest_departure">
                  Earliest Departure
                </label>

                <input
                  id="earliest_departure"
                  type="time"
                  name="earliest_departure"
                  required
                  value={preferences.earliest_departure}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="latest_arrival">
                  Latest Arrival
                </label>

                <input
                  id="latest_arrival"
                  type="time"
                  name="latest_arrival"
                  required
                  value={preferences.latest_arrival}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group checkbox-group">

                <label htmlFor="allow_overnight_flights">
                  Allow Overnight Flights
                </label>

                <input
                  id="allow_overnight_flights"
                  type="checkbox"
                  name="allow_overnight_flights"
                  checked={preferences.allow_overnight_flights}
                  onChange={handleChange}
                />

              </div>

              <div className="form-group">
                <label htmlFor="travel_style">
                  Travel Style
                </label>

                <select
                  id="travel_style"
                  name="travel_style"
                  value={preferences.travel_style}
                  onChange={handleChange}
                >
                  <option value="budget">Budget</option>
                  <option value="balanced">Balanced</option>
                  <option value="time-focused">Time-Focused</option>
                </select>
              </div>

              <button
                type="submit"
                className="start-button"
                disabled={loading}
              >
                {loading ? "Searching..." : "Find My Trip"}
              </button>

              <button
                type="button"
                className="back-button"
                onClick={() => setShowForm(false)}
              >
                Back
              </button>

            </form>
            {/* ------------------------------------------
                API Response
            ------------------------------------------ */}

            {error && (
              <div className="error-message">
                <p>{error}</p>
              </div>
            )}

            {results && (
              <div className="result-container">

                <h2>Recommendations Received!</h2>

                <p>
                  The recommendation engine
                  successfully processed your request.
                </p>

                <p>
                  Pareto-optimal trips:{" "}
                  {results.meta?.pareto_count ?? "N/A"}
                </p>

                <details>
                  <summary>View API Response</summary>

                  <pre>
                    {JSON.stringify(results, null, 2)}
                  </pre>
                </details>

              </div>
            )}
          </div>

        )}

      </main>

      <footer className="footer">
        <p>© 2026 Student Trip Optimizer</p>
      </footer>

    </div>
  );
}

export default App;
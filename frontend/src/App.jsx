import { useState } from "react";
import "./App.css";
import RecommendationResults from "./components/RecommendationResults";
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";
// ------------------------------------------
// Student Trip Optimizer
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
  origin: "MEL",
  destination: "SYD",
  departure_date: "2026-11-10",
  return_date: "2026-11-13",

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
  // ------------------------------------------
  // Validate User Input
  // ------------------------------------------

  const budget = Number(preferences.max_budget);

  if (
    preferences.max_budget === "" ||
    !Number.isFinite(budget) ||
    budget <= 0
  ) {
    setError("Please enter a valid budget greater than 0.");
    setResults(null);
    return;
  }

  if (preferences.origin === preferences.destination) {
  setError("Origin and destination must be different.");
  setResults(null);
  return;
  }

  if (
  !preferences.departure_date ||
  !preferences.return_date ||
  preferences.return_date <= preferences.departure_date
  ) {
  setError("Return date must be after departure date.");
  setResults(null);
  return;
}


const isDemoSearch =
  preferences.origin === "MEL" &&
  preferences.destination === "SYD" &&
  preferences.departure_date === "2026-11-10" &&
  preferences.return_date === "2026-11-13"

if (!isDemoSearch) {
  setError(
    "Demo Mode currently supports only MEL → SYD, " +
    "10–13 November 2026. Live flight search is coming later."
  );
  setResults(null);
  return;
}


  // ------------------------------------------
  // Reset Search State
  // ------------------------------------------

  setLoading(true);
  setError("");
  setResults(null);

  try {
    // Keep the same API URL and request payload
    // that worked in V6.2.
     
    const response = await fetch(
      `${API_BASE_URL}/recommendations`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...preferences,
          max_budget: Number(preferences.max_budget),
        }),
      }
    );


    if (!response.ok) {
      throw new Error(
        `Unable to get recommendations (${response.status}).`
      );
    }

    const data = await response.json();

    if (data.status !== "success") {
      throw new Error("Unexpected API response.");
    }

    setResults(data);
  } catch (err) {
    setError(
      err instanceof Error
        ? err.message
        : "Something went wrong. Please try again."
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
            
            {/* V6.7 — Travel Search */}

            <div className="form-group">
              <label htmlFor="origin">Origin Airport</label>
              <select
                id="origin"
                name="origin"
                value={preferences.origin}
                onChange={handleChange}
                required
              >
                <option value="MEL">Melbourne (MEL)</option>
                <option value="SYD">Sydney (SYD)</option>
                <option value="BNE">Brisbane (BNE)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="destination">Destination Airport</label>
              <select
                id="destination"
                name="destination"
                value={preferences.destination}
                onChange={handleChange}
                required
              >
                <option value="MEL">Melbourne (MEL)</option>
                <option value="SYD">Sydney (SYD)</option>
                <option value="BNE">Brisbane (BNE)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="departure_date">Departure Date</label>
              <input
                id="departure_date"
                type="date"
                name="departure_date"
                value={preferences.departure_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="return_date">Return Date</label>
              <input
                id="return_date"
                type="date"
                name="return_date"
                min={preferences.departure_date}
                value={preferences.return_date}
                onChange={handleChange}
                required
              />
            </div>
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
                disabled={loading}
                aria-busy={loading}
              >
                {loading ? "Finding Trips..." : "Find My Trip"}
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
                Search Feedback
            ------------------------------------------ */}

            {loading && (
              <div className="search-feedback" role="status">
                <span className="loading-spinner" aria-hidden="true" />
                <div>
                  <strong>Finding your best trips...</strong>
                  <p>
                    Comparing prices, flight times and travel value.
                  </p>
                </div>
              </div>
            )}

            {error && (
              <div className="search-feedback error-feedback" role="alert">
                <strong>Something went wrong</strong>
                <p>{error}</p>
                <p>Please try again or check your connection.</p>
              </div>
            )}

            {!loading && !error && results && (
              <RecommendationResults results={results} />
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
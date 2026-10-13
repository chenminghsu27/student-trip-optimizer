import "./App.css";

// ------------------------------------------
// Student Trip Optimizer Homepage
//
// Display the main landing page
// for the travel recommendation system.
// ------------------------------------------

function App() {
  return (
    <div className="app">

      <header className="navbar">
        <h2>✈ Student Trip Optimizer</h2>
      </header>

      <main className="hero">

        <div className="hero-content">

          <span className="badge">
            Travel Smarter, Spend Less
          </span>

          <h1>
            Find Your Perfect Trip
          </h1>

          <p>
            Compare flights and accommodation
            based on your budget, travel time,
            and personal preferences.
          </p>

          <button className="start-button">
            Get Started
          </button>

        </div>

      </main>

      <footer className="footer">
        <p>
          © 2026 Student Trip Optimizer
        </p>
      </footer>

    </div>
  );
}

export default App;
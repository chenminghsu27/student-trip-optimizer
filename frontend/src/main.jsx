import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App.jsx";
import "./index.css";

// ------------------------------------------
// React Application Entry Point
//
// Render the App component
// inside the root HTML element.
// ------------------------------------------

ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

# ✈️ Student Trip Optimizer

**A full-stack travel recommendation system that helps students balance travel costs, usable travel time, and personal preferences.**

## 📖 Overview

Finding the cheapest flight does not always mean finding the best trip.

A late-night departure or an early-morning return may reduce ticket costs but also significantly reduce the time available to enjoy a destination.

Student Trip Optimizer addresses this problem by comparing flight and accommodation combinations using multiple factors rather than price alone.

The application helps users understand the trade-offs between affordability, travel convenience, and usable travel hours.

## ✨ Key Features

- **Trip Recommendations:** Compare combinations of round-trip flights and accommodation.
- **Pareto Optimization:** Identify travel options that are not dominated by alternatives across cost and usable travel time.
- **Weighted Scoring:** Adjust recommendations based on budget-focused, balanced, or time-focused travel preferences.
- **Cost per Usable Hour:** Evaluate how much each hour of usable travel time costs.
- **Travel Preferences:** Configure budget, departure and arrival time preferences, and overnight flight allowance.
- **Search Validation:** Validate airport codes, travel dates, budgets, and time formats.
- **Responsive Frontend:** Display trip comparisons and recommendations through a React interface.
- **Automated Testing:** Use Pytest to verify recommendation logic, API behaviour, data validation, and regression scenarios.

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, JavaScript, Vite, CSS |
| Backend | Python, FastAPI |
| Data Validation | Pydantic, TypedDict |
| Algorithms | Pareto Optimization, Weighted Scoring |
| Testing | Pytest, FastAPI TestClient |
| Version Control | Git, GitHub |

## 🏗️ System Architecture

```text
React Frontend
      |
      | HTTP POST /recommendations
      v
FastAPI Backend
      |
      v
Request Validation
      |
      v
Flight & Hotel Data Validation
      |
      v
Recommendation Engine
      |
      |-- Price Calculation
      |-- Usable Travel Hours
      |-- Flight Penalties
      |-- Weighted Scoring
      |-- Pareto Optimization
      |
      v
JSON Response
      |
      v
Recommendation Cards & Trip Comparison
```

## 🧠 Recommendation Approach

### 1. Total Trip Cost

The system combines round-trip flight prices and accommodation costs to estimate the overall trip budget.

### 2. Usable Travel Hours

Instead of considering only the number of days between departure and return, the application calculates the time realistically available at the destination.

### 3. Pareto Optimization

The recommendation engine compares travel alternatives across competing objectives, such as minimizing cost and maximizing usable travel time.

Pareto optimization helps identify options where improving one objective would require sacrificing another.

### 4. Weighted Scoring

Users can choose between three travel styles:

- **Budget:** Prioritizes affordability.
- **Balanced:** Balances price and usable travel time.
- **Time-Focused:** Places greater emphasis on maximizing travel time.

### 5. Cost per Usable Hour

The application also calculates:

\[
\text{Cost per Usable Hour} = \frac{\text{Total Trip Cost}}{\text{Usable Travel Hours}}
\]

This provides an additional way to compare the value of different trips.

## 📁 Project Structure

```text
student-trip-optimizer/
├── backend/
│   ├── api.py
│   ├── data.py
│   ├── data_validator.py
│   ├── models.py
│   ├── recommendation_engine.py
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## 🚀 Running Locally

### Backend

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m uvicorn api:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### Frontend

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

Open the local URL displayed by Vite, typically:

`http://localhost:5173`

## 🧪 Testing

Run the backend test suite:

```bash
cd backend
python -m pytest -q
```

**Latest verified local result: 92 tests passed.**

The tests cover pricing calculations, recommendation behaviour, data validation, API responses, and regression scenarios.

## ⚠️ Current Limitations

This project is currently a demonstration MVP.

- Flight and accommodation information comes from predefined mock data.
- The demonstration search currently supports Melbourne (MEL) to Sydney (SYD), 10–13 November 2026.
- Recommendations are designed for individual travellers.
- Real-time flight prices, accommodation availability, and bookings are not yet supported.

## 🗺️ Future Improvements

- Integrate live flight data through an external API.
- Support additional destinations and flexible travel dates.
- Integrate real accommodation pricing and availability.
- Improve filtering and recommendation explanations.
- Deploy the frontend and backend for public access.

## 🎯 Project Motivation

This project was developed to explore how software engineering and optimization algorithms can solve a practical travel-planning problem.

It combines full-stack development, API design, data modelling, automated testing, and multi-objective decision-making in a single application.

The long-term goal is to help budget-conscious travellers make more informed decisions by considering not only how much a trip costs, but also how much usable travel time it provides.

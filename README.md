# ✈️ FlyHigh AI Travel Chatbot

FlyHigh is an AI-powered backend service that integrates with the Amadeus flight API to search and display real-time flight schedules. It uses FastAPI and an LLM agent to interpret natural language flight queries.

---

## 🚀 Features

* AI chatbot for natural language flight search
* Real-time flight schedule lookup via Amadeus API
* OAuth token generation using environment credentials
* Modular FastAPI backend
* JSON-based booking storage
* Clean service architecture

---

## 📁 Project Structure

```
flyhigh/
├── main.py
├── routers/
│   └── chat.py
├── services/
│   ├── ai_agent.py
│   ├── flights_service.py
│   ├── auth_service.py
│   └── storage.py
├── data/
│   └── bookings.json
├── .env
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install fastapi uvicorn requests python-dotenv openai
```

### 2. Configure environment variables

Create a `.env` file:

```
AMADEUS_CLIENT_ID=your_client_id
AMADEUS_CLIENT_SECRET=your_client_secret
OPENAI_API_KEY=your_openai_key
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔍 Flight Search API

### Endpoint

```
GET /chat
```

The chatbot interprets user input and calls the Amadeus schedule API.

---

## 🧪 Example: Curl Flight Schedule Search

```bash
curl -X GET \
"https://test.api.amadeus.com/v2/schedule/flights?carrierCode=EK&flightNumber=380&scheduledDepartureDate=2026-03-10" \
-H "accept: application/vnd.amadeus+json" \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🤖 Example Chatbot Queries

### 1. Search specific flight

**User:**

```
Show EK380 flight on March 10
```

**Bot response:**

```
Emirates EK380
Dubai → Hong Kong
Departure: 10:40 AM
Arrival: 9:50 PM
Duration: 7h 10m
Aircraft: Airbus A380
```

---

### 2. Route search

**User:**

```
List Emirates flights from Mumbai to Dubai
```

**Bot response:**

```
Available Emirates flights:

EK501 — 04:00 → 05:45
EK503 — 09:35 → 11:20
EK507 — 21:50 → 23:35
```

---

## 📦 Example JSON Flight Response (Simplified)

```json
{
  "flight": "EK380",
  "route": "DXB → HKG",
  "departure": "10:40",
  "arrival": "21:50",
  "duration": "7h 10m",
  "aircraft": "A380"
}
```

---

## 🔐 Authentication Flow

1. Backend generates OAuth token via `auth_service.py`
2. Token is used for Amadeus API calls
3. Token is refreshed automatically when expired

---

## 🧠 Architecture Overview

```
User → AI Agent → Flight Service → Auth Service → Amadeus API
```

The AI agent extracts flight parameters and routes requests to backend services.

---

## ⚠️ Notes

* Amadeus test API has rate limits
* Token expires ~30 minutes
* Production systems should cache tokens
* Use async HTTP clients for scalability

---

## 🔮 Possible Future Improvements

* Redis token caching
* Async httpx integration
* Flight price comparison
* Booking workflows
* Conversation memory
* Deployment with Docker/Kubernetes

---

## Author

Jay Sanghavi

GitHub: https://github.com/JaySanghavi

# Amazon Seller Analytics Dashboard — Build Walkthrough

A portfolio project that pulls synthetic Amazon seller data (orders, inventory,
ad spend) into a dashboard showing revenue trends, inventory reorder alerts,
and ad ROAS by product.

## Tech Stack & Why

| Layer | Choice | Why |
|---|---|---|
| Backend | **FastAPI** (Python) | Fast to write, auto-generates interactive API docs at `/docs`, async-ready, and Python is a strong pairing with your data/domain background |
| Database | **SQLite** (dev) → **Postgres** (prod) | SQLite needs zero setup locally. SQLAlchemy makes swapping to Postgres for deployment a one-line config change |
| ORM | **SQLAlchemy** | Industry-standard, and knowing it is genuinely useful for interviews |
| Frontend | **React + Vite** | Vite is fast to set up and is what most modern freelance/job postings expect over older tooling |
| Styling | **Tailwind CSS** | Lets you build clean UI fast without writing custom CSS files |
| Charts | **Recharts** | Simple React-native charting, good enough for a polished dashboard without extra complexity |
| Synthetic data | **Faker** (Python) | Real Amazon SP-API access requires seller approval — synthetic data with realistic patterns (trend, noise, restocks) is the pragmatic, honest choice for a portfolio project |

## Project Structure

```
amazon-seller-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entrypoint + CORS setup
│   │   ├── database.py          # DB connection/session setup
│   │   ├── models/models.py     # SQLAlchemy tables: Product, Order, InventorySnapshot, AdSpend
│   │   ├── schemas/schemas.py   # Pydantic response shapes
│   │   └── routers/
│   │       ├── products.py      # GET /products
│   │       └── analytics.py     # The core aggregation logic (see below)
│   ├── scripts/generate_data.py # Synthetic data generator
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx               # Wires everything together
    │   ├── api/client.js         # Centralized API calls
    │   └── components/
    │       ├── KpiCards.jsx
    │       ├── RevenueTrendChart.jsx
    │       ├── InventoryAlerts.jsx
    │       └── AdPerformance.jsx
    └── package.json
```

## The Data Model (why it's structured this way)

Four tables, all referencing `Product`:
- **Product** — the anchor entity (ASIN, name, cost, price, restock lead time)
- **Order** — one row per product per day with sales
- **InventorySnapshot** — daily stock level per product
- **AdSpend** — daily ad spend, clicks, impressions, and attributed sales per product

This mirrors how a real seller's data is actually shaped, and it's a good
thing to be able to sketch on a whiteboard in an interview — it shows you
think about schema design, not just "get data on screen."

## The "Smart" Feature: Reorder Point Calculation

Instead of just showing raw stock numbers, `/analytics/inventory-alerts`
calculates:

```
daily_velocity = units sold in last 14 days / 14
reorder_point = daily_velocity * lead_time_days * 1.2   (20% safety buffer)
needs_reorder = current_stock <= reorder_point
```

This is a simplified version of a real reorder-point formula. Being able to
explain *why* you added a 20% buffer, and what you'd improve with real data
(e.g. accounting for seasonality) is exactly the kind of thing that makes a
portfolio project stand out over a basic CRUD app.

## How to Run It Locally

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m scripts.generate_data # generates ~90 days of synthetic data
uvicorn app.main:app --reload   # runs on http://localhost:8000
```

Visit `http://localhost:8000/docs` — FastAPI auto-generates interactive API
docs where you can test every endpoint. This alone is worth showing off in
a demo video or screenshot.

**Frontend (separate terminal):**
```bash
cd frontend
npm install
npm run dev                      # runs on http://localhost:5173
```

Open `http://localhost:5173` — you should see the full dashboard populated
with data from the backend.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /products` | List all products |
| `GET /analytics/kpi-summary` | Top-line 30-day KPIs for the header cards |
| `GET /analytics/revenue-trend?days=30` | Daily revenue/units time series |
| `GET /analytics/inventory-alerts` | Reorder point calc per product |
| `GET /analytics/ad-performance?days=30` | ROAS per product |

## Deployment (once it works locally)

1. **Backend** → Render or Railway (free tier). Set `DATABASE_URL` env var
   to a Postgres connection string from Supabase or Neon (also free tier).
   Run `generate_data.py` once against the prod DB, or add a startup hook.
2. **Frontend** → Vercel. Set `VITE_API_BASE_URL` env var to your deployed
   backend URL.
3. Update the CORS `allow_origins` in `backend/app/main.py` to your actual
   deployed frontend URL instead of `*`.

## What to Put in Your Portfolio Write-up

- The problem this solves (sellers manually tracking spreadsheets, missing
  reorder windows, not knowing which ads are actually profitable)
- A screenshot/GIF of the live dashboard
- The schema diagram (even a simple boxes-and-arrows sketch)
- One paragraph on the reorder-point logic and why you chose that formula
- Honest note that data is synthetic, and what you'd change with real
  SP-API access (e.g. handling API rate limits, OAuth flow, webhooks for
  real-time inventory updates)

## Next Steps to Extend This (optional, for a v2)

- Add product-level detail pages (click a product → see its own trend charts)
- Add authentication so it's a real multi-user app
- Add a "listing quality score" feature (ties into the second portfolio
  project — you can reuse this same data model)
- Write actual unit tests for the reorder-point logic (`pytest`) — testing
  is something a lot of portfolio projects skip and it stands out when you
  have it

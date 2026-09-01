# Amazon Seller Analytics Dashboard

Dashboard for Amazon sellers that pulls order, inventory, and ad spend data
together so you can see revenue trends, low-stock alerts, and ad ROAS in
one place instead of digging through separate reports.

## Stack

- Backend: FastAPI, SQLAlchemy, SQLite (works with Postgres too)
- Frontend: React, Vite, Tailwind, Recharts
- Data is synthetic (generated with Faker) since real Amazon SP-API access
  needs seller approval

## Structure

```
backend/
  app/
    main.py            FastAPI app + CORS
    database.py         DB setup
    models/models.py    Product, Order, InventorySnapshot, AdSpend
    schemas/schemas.py  response models
    routers/
      products.py
      analytics.py       main aggregation logic
  scripts/generate_data.py

frontend/
  src/
    App.jsx
    api/client.js
    components/
      KpiCards.jsx
      RevenueTrendChart.jsx
      InventoryAlerts.jsx
      AdPerformance.jsx
```

## Data model

Product is the main table. Order, InventorySnapshot, and AdSpend all point
back to it — one row per product per day.

## Reorder alerts

```
daily_velocity = units sold in last 14 days / 14
reorder_point  = daily_velocity * lead_time_days * 1.2
needs_reorder  = current_stock <= reorder_point
```

Flags products likely to run out before a restock would arrive.

## Running it

Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m scripts.generate_data
uvicorn app.main:app --reload
```
Runs on localhost:8000, docs at localhost:8000/docs

Frontend (new terminal):
```bash
cd frontend
npm install
npm run dev
```
Runs on localhost:5173

## Endpoints

- GET /products
- GET /analytics/kpi-summary
- GET /analytics/revenue-trend?days=30
- GET /analytics/inventory-alerts
- GET /analytics/ad-performance?days=30

## Deploying

Backend on Render/Railway, Postgres from Supabase/Neon, frontend on Vercel.
Set DATABASE_URL on the backend and VITE_API_BASE_URL on the frontend, and
update CORS origins in main.py.

## TODO

- product detail pages
- auth
- listing quality score
- tests

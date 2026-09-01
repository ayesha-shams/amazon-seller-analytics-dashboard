from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import products, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Amazon Seller Analytics Dashboard API",
    description="Aggregated sales, inventory, and ad performance data for e-commerce sellers.",
    version="0.1.0",
)

# Allow the local Vite dev server (and later, your deployed frontend) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # tighten this for production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Amazon Seller Dashboard API is running"}

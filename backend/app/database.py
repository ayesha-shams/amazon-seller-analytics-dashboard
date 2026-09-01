"""
Database connection setup.

Uses SQLite for local dev simplicity. To upgrade to Postgres for deployment,
just change DATABASE_URL to a postgres:// connection string (e.g. from
Supabase or Neon) -- SQLAlchemy handles the rest with no code changes needed
elsewhere in the app.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./seller_dashboard.db")

# check_same_thread=False is only needed for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

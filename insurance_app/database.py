import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# If you also want to use the `databases` package for async access, keep this import:
try:
    from databases import Database  # optional
except Exception:
    Database = None  # makes this optional

# Load environment variables
load_dotenv()

# Expect something like:
#   postgresql+psycopg2://USER:PASS@HOST:PORT/DBNAME
# If you are using the `databases` package (async), that URL usually looks like:
#   postgresql+asyncpg://USER:PASS@HOST:PORT/DBNAME
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost/dbname")

# --- SQLAlchemy ORM (sync) ---
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # helps avoid stale connections
    pool_recycle=1800,    # recycle every 30 minutes
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# FastAPI dependency for a DB session
def get_db():
    """
    Yield a SQLAlchemy Session for use in FastAPI dependencies:
        def endpoint(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Optional: async Database instance (only if you need it) ---
# If you use `databases` for async queries, keep this available:
if Database is not None:
    database = Database(DATABASE_URL.replace("+psycopg2", "+asyncpg")) if "+psycopg2" in DATABASE_URL else Database(DATABASE_URL)

    async def get_database():
        """
        Optional FastAPI dependency for the `databases` package:
            async def endpoint(db = Depends(get_database)): ...
        Ensures the connection is available within the request context.
        """
        # Most apps manage connect/disconnect in startup/shutdown events.
        # This helper simply returns the handle if you prefer per-request injection.
        return database

__all__ = ["engine", "SessionLocal", "Base", "get_db", "database", "get_database"]



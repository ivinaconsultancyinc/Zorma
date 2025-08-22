from databases import Database
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Async database connection
database = Database(DATABASE_URL)

# SQLAlchemy base class for models
Base = declarative_base()

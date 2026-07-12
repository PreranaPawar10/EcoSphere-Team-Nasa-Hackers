import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# backend/ directory
backend_directory = Path(__file__).resolve().parents[2]

# backend/.env
env_path = backend_directory / ".env"

load_dotenv(env_path)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError(
        f"DATABASE_URL is missing. Add it to {env_path}"
    )


engine = create_engine(
    database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
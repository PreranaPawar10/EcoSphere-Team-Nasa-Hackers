from fastapi import FastAPI
from sqlalchemy import text

from app.database.db import engine
from app.routers import (
    api_router,
    special_router,
)


app = FastAPI(
    title="EcoSphere ESG Management Platform",
    description=(
        "Backend API for Environmental, Social and "
        "Governance management."
    ),
    version="1.0.0",
)


@app.get(
    "/",
    tags=["System"],
    summary="Backend health check",
)
def root():
    return {
        "message": "EcoSphere Backend is running successfully."
    }


@app.get(
    "/db-test",
    tags=["System"],
    summary="Test PostgreSQL connection",
)
def db_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        return {
            "database": "Connected",
            "result": result.scalar_one(),
        }


app.include_router(
    api_router,
    prefix="/api/v1",
)

app.include_router(
    special_router,
    prefix="/api/v1",
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text, inspect

from app.database import engine, Base

from app.api import (
    cases,
    search,
    suspects,
    reports,
    analytics,
    ai
)


# ============================================================
# DATABASE SETUP
# ============================================================

# Create tables that do not already exist
Base.metadata.create_all(bind=engine)


# ============================================================
# TIMELINE DATABASE MIGRATION
# ============================================================

def migrate_timeline_table():

    required_columns = {
        "event_type": "TEXT",
        "location": "TEXT",
        "latitude": "TEXT",
        "longitude": "TEXT",
        "source": "TEXT",
        "confidence": "TEXT"
    }

    inspector = inspect(engine)

    # Check whether timeline table exists
    existing_tables = inspector.get_table_names()

    if "timeline" not in existing_tables:
        return

    # Get existing columns
    existing_columns = {
        column["name"]
        for column in inspector.get_columns("timeline")
    }

    # Add missing columns
    with engine.begin() as connection:

        for column_name, column_type in required_columns.items():

            if column_name not in existing_columns:

                connection.execute(
                    text(
                        f"ALTER TABLE timeline "
                        f"ADD COLUMN {column_name} {column_type}"
                    )
                )


# Run migration when backend starts
migrate_timeline_table()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Investigation Copilot",
    description="AI-powered investigation and case analysis backend",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://192.168.0.102:3000",
        "https://ai-investigation-copilot.vercel.app"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(cases.router)

app.include_router(search.router)

app.include_router(suspects.router)

app.include_router(reports.router)

app.include_router(analytics.router)

app.include_router(ai.router)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Investigation Copilot Backend Running"
    }
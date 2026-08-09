from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api import (
    cases,
    search,
    suspects,
    reports,
    analytics,
    ai
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Investigation Copilot",
    description="AI-powered investigation and case analysis backend",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.0.102:3000",
        "https://ai-investigation-copilot.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------

app.include_router(cases.router)
app.include_router(search.router)
app.include_router(suspects.router)
app.include_router(reports.router)
app.include_router(analytics.router)
app.include_router(ai.router)


# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AI Investigation Copilot Backend Running"
    }
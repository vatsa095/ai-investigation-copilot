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

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Investigation Copilot"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://192\.168\.0\.102:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases.router)
app.include_router(search.router)
app.include_router(suspects.router)
app.include_router(reports.router)
app.include_router(analytics.router)
app.include_router(ai.router)


@app.get("/")
def home():
    return {
        "message": "AI Investigation Copilot Backend Running"
    }
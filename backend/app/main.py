import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.cache import get_cached_report, set_cached_report
from app.config import settings  # noqa: F401 — validates env vars at import time
from app.models import InsightReport, InsightRequest
from app.services.llm import synthesize
from app.services.news import fetch_all_news

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # settings import above raises ValueError on startup if any required var is missing
    yield


app = FastAPI(title="Bain Company Intelligence Tool", lifespan=lifespan)

ALLOWED_ORIGINS = [
    "https://bain-and-company-insights-a2p8y5yzt.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/insights", response_model=InsightReport)
async def get_insights(request: InsightRequest) -> InsightReport:
    cached_report = get_cached_report(request.company)
    if cached_report:
        logger.info("Cache hit for company: %s", request.company)
        return InsightReport(**cached_report)

    articles = await fetch_all_news(request.company)
    if not articles:
        raise HTTPException(
            status_code=503,
            detail=f"No news articles found for '{request.company}'. Try again later.",
        )

    raw_report = await synthesize(articles, request.company)
    set_cached_report(request.company, raw_report)

    return InsightReport(**raw_report)

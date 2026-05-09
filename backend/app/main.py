from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings  # noqa: F401 — validates env vars at import time
from app.models import InsightReport, InsightRequest, RiskFlag, Source, StrategicTheme, ValueCreationHypothesis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # settings import above raises ValidationError on startup if any required var is missing
    yield


app = FastAPI(title="Bain Company Intelligence Tool", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/insights", response_model=InsightReport)
async def get_insights(request: InsightRequest) -> InsightReport:
    return InsightReport(
        company=request.company,
        executive_summary=(
            f"{request.company} is navigating a pivotal growth inflection, expanding its core platform "
            "while facing margin pressure from rising infrastructure costs and intensifying competition."
        ),
        investment_thesis=(
            f"{request.company} represents a compelling platform consolidation play with durable "
            "switching costs, underpenetrated enterprise verticals, and a credible path to margin expansion "
            "through operational leverage as growth normalises."
        ),
        bull_case=[
            "Enterprise pipeline conversion accelerating into Q3, indicating product-market fit at scale.",
            "International expansion into EMEA tracking ahead of internal targets.",
            "Gross margin trajectory supports 30%+ EBITDA margin at steady state.",
        ],
        bear_case=[
            "Elevated CAC and lengthening sales cycles signal go-to-market inefficiency.",
            "Well-capitalised incumbents accelerating feature parity, compressing differentiation window.",
            "Regulatory scrutiny in core markets could impair data monetisation strategy.",
        ],
        strategic_themes=[
            StrategicTheme(
                theme="Platform consolidation",
                evidence="Three bolt-on acquisitions in the past 18 months expanding data and workflow capabilities.",
                sources=[1, 2],
            ),
            StrategicTheme(
                theme="Enterprise up-market motion",
                evidence="ACV for new enterprise logos up materially year-over-year; dedicated enterprise sales org stood up.",
                sources=[3],
            ),
        ],
        risk_flags=[
            RiskFlag(
                category="Competitive",
                severity="High",
                rationale="Primary competitor announced a directly competing product suite at its annual conference.",
                sources=[2],
            ),
            RiskFlag(
                category="Macro",
                severity="Medium",
                rationale="IT budget freezes at financial-services customers may delay Q4 pipeline conversion.",
                sources=[4],
            ),
        ],
        value_creation_hypotheses=[
            ValueCreationHypothesis(
                lever="Sales efficiency",
                hypothesis="Restructuring the mid-market segment under a PLG motion reduces CAC by a third.",
                evidence="Peer benchmarks show PLG-led mid-market cohorts convert at lower cost.",
                test="Pilot PLG funnel for one product line in Q3 and track 90-day CAC vs. current direct-sales cohort.",
            ),
            ValueCreationHypothesis(
                lever="Pricing power",
                hypothesis="Introducing usage-based pricing unlocks consumption expansion revenue from existing accounts.",
                evidence="NRR for usage-billed peers consistently exceeds seat-licence peers by 15–20 points.",
                test="Run A/B pricing experiment with a subset of SMB renewals in next quarter.",
            ),
        ],
        sources=[
            Source(
                id=1,
                title=f"{request.company} Completes Acquisition of DataBridge Analytics",
                publisher="Business Wire",
                published_at="2026-04-15T09:00:00Z",
                url="https://example.com/articles/1",
            ),
            Source(
                id=2,
                title="Competitor Unveils End-to-End Platform at Annual Summit",
                publisher="TechCrunch",
                published_at="2026-04-20T14:30:00Z",
                url="https://example.com/articles/2",
            ),
            Source(
                id=3,
                title=f"{request.company} Reports Record Enterprise Bookings in Q1",
                publisher="Reuters",
                published_at="2026-04-28T11:00:00Z",
                url="https://example.com/articles/3",
            ),
            Source(
                id=4,
                title="Financial Services IT Spending Outlook Dims Amid Rate Uncertainty",
                publisher="Financial Times",
                published_at="2026-05-01T08:00:00Z",
                url="https://example.com/articles/4",
            ),
        ],
        generated_at=datetime.now(timezone.utc).isoformat(),
        confidence_caveats=(
            "This brief is based on publicly available news sources from the past 30 days. "
            "It does not incorporate proprietary data, management interviews, or financial filings. "
            "Treat as directional context only."
        ),
    )

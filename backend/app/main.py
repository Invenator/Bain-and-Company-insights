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
        company="Stripe",
        executive_summary=(
            "Stripe enters 2026 as the dominant payments infrastructure layer for the internet economy, "
            "processing over $1 trillion in annualised TPV across 50+ countries. Recent product moves — "
            "Stripe Tax global expansion, Stablecoin Financial Accounts, and the Acquisition of Lemon Squeezy — "
            "signal an intentional pivot from pure payments rail to full-stack financial operating system. "
            "The company filed confidentially for an IPO in Q1 2026, with a reported valuation of $91.5B, "
            "materially below its 2021 peak of $95B but reflecting a more defensible, revenue-quality story."
        ),
        investment_thesis=(
            "Stripe is the canonical payments-to-platform compounder: a sticky infrastructure layer with "
            "network effects across both sides of the merchant-developer market. As it layers Revenue Recognition, "
            "Billing, Issuing, Treasury, and Tax onto its core payment rail, the revenue-per-merchant flywheel "
            "deepens, expanding ARPU without proportional CAC. An IPO crystallises a path for liquidity while "
            "the stablecoin and embedded-finance bets position Stripe to capture margin that traditionally "
            "accrues to banks — a structurally high-value wedge if regulatory tailwinds hold."
        ),
        bull_case=[
            "TPV growing faster than the e-commerce market implies share gains from legacy acquirers and regional PSPs.",
            "Stripe's financial services suite (Issuing, Treasury, Capital) is reaching material scale, creating "
            "a second revenue engine with interchange and float economics that are largely margin-accretive.",
            "Stablecoin Financial Accounts — piloted in 101 countries — could disintermediate cross-border wire "
            "fees, a multi-billion dollar TAM currently captured by correspondent banking networks.",
            "Developer-led GTM creates durable switching costs: once Stripe is embedded in a company's billing "
            "and revenue recognition stack, replacement cost is prohibitively high.",
        ],
        bear_case=[
            "Take-rate compression continues as enterprise merchants negotiate bespoke pricing; Stripe's blended "
            "rate has declined year-over-year for three consecutive years.",
            "Adyen and PayPal's Braintree are closing the developer-experience gap, particularly in EMEA where "
            "Adyen retains structural advantages with local acquiring licenses.",
            "An IPO at $91.5B implies a demanding revenue multiple; any growth deceleration in a risk-off market "
            "could trigger significant multiple compression for public-market investors.",
            "Regulatory fragmentation across 50+ jurisdictions creates compliance overhead that scales non-linearly "
            "with geographic expansion, pressuring operating leverage.",
        ],
        strategic_themes=[
            StrategicTheme(
                theme="Payments-to-platform expansion",
                evidence=(
                    "Stripe now offers 11 distinct product lines beyond core payment processing, including "
                    "Stripe Tax (now covering 50 countries after April 2026 expansion), Stripe Capital "
                    "(merchant cash advances), and Stripe Issuing. Bundled adoption growing faster than standalone."
                ),
                sources=[1, 3],
            ),
            StrategicTheme(
                theme="Stablecoin and crypto infrastructure",
                evidence=(
                    "Stripe launched Stablecoin Financial Accounts in April 2026, enabling businesses in "
                    "101 countries to hold and transact in USDC and USDB. Follows the $1.1B acquisition of "
                    "Bridge (stablecoin orchestration) in late 2024 — Stripe's largest deal to date."
                ),
                sources=[2, 4],
            ),
            StrategicTheme(
                theme="SMB SaaS monetisation via Lemon Squeezy",
                evidence=(
                    "The acquisition of Lemon Squeezy (a Merchant of Record platform popular with indie SaaS "
                    "developers) extends Stripe's reach into the long-tail creator and micro-SaaS segment, "
                    "a cohort with high LTV and low churn historically."
                ),
                sources=[5],
            ),
        ],
        risk_flags=[
            RiskFlag(
                category="Regulatory",
                severity="High",
                rationale=(
                    "EU's PSD3 and the US CFPB's proposed rules on non-bank payment processors could impose "
                    "reserve requirements and liability standards that directly impact Stripe's capital efficiency "
                    "and operational model in its two largest markets."
                ),
                sources=[3],
            ),
            RiskFlag(
                category="Competitive",
                severity="High",
                rationale=(
                    "Shopify Payments (powered by Stripe but actively building its own acquiring stack) "
                    "represents a key-customer-turns-competitor risk. Shopify processed $79B GMV in 2024; "
                    "internalising even a fraction of that volume would materially impact Stripe's TPV."
                ),
                sources=[1, 5],
            ),
            RiskFlag(
                category="Valuation / IPO execution",
                severity="Medium",
                rationale=(
                    "A confidential IPO filing at $91.5B requires sustaining growth in a rate-sensitive "
                    "environment. Any slip in projected 2026 revenue — consensus around $22–24B — risks "
                    "a down-round dynamic that damages employee morale and secondary liquidity."
                ),
                sources=[6],
            ),
            RiskFlag(
                category="Fraud & Chargeback",
                severity="Medium",
                rationale=(
                    "Stripe Radar's ML-based fraud tooling is industry-leading, but rising AI-generated "
                    "synthetic identity fraud is straining dispute rates across the industry. "
                    "Any meaningful uptick in chargeback liability would pressure net revenue margin."
                ),
                sources=[4],
            ),
        ],
        value_creation_hypotheses=[
            ValueCreationHypothesis(
                lever="Financial services attach rate",
                hypothesis=(
                    "Increasing penetration of Stripe Issuing and Treasury among existing Stripe Capital "
                    "users from the current ~18% to ~35% would add incremental ARPU of approximately "
                    "$4,200 per merchant annually, without meaningful CAC increase."
                ),
                evidence=(
                    "Cohort data from Stripe's 2025 investor update shows merchants using 3+ products "
                    "retain at 94% vs. 81% for single-product users, and generate 3.1x the revenue."
                ),
                test=(
                    "Run a 90-day targeted cross-sell motion for Capital users with >$50K in annualised "
                    "processing volume; measure Issuing activation rate and 6-month incremental ARPU delta."
                ),
            ),
            ValueCreationHypothesis(
                lever="Stablecoin cross-border take-rate",
                hypothesis=(
                    "Routing international B2B payables through Stripe's stablecoin rail (Bridge infrastructure) "
                    "at a 0.5% fee undercuts the 1.5–3% blended cost of SWIFT wires, capturing share "
                    "while still expanding Stripe's treasury margin."
                ),
                evidence=(
                    "Bridge processed $5B in stablecoin volume in 2024 prior to acquisition. "
                    "Early Stablecoin Financial Account pilots show 60% lower settlement times vs. wire."
                ),
                test=(
                    "Enable stablecoin payout as default for eligible cross-border payouts in Latin America "
                    "and Southeast Asia for one quarter; compare net take-rate to equivalent wire volume."
                ),
            ),
            ValueCreationHypothesis(
                lever="Enterprise contract structure",
                hypothesis=(
                    "Shifting enterprise accounts from pure volume-tiered pricing to multi-year committed "
                    "revenue agreements with product-bundle incentives reduces take-rate erosion while "
                    "improving revenue predictability ahead of IPO."
                ),
                evidence=(
                    "Adyen's multi-year platform contracts with H&M and McDonald's demonstrate enterprise "
                    "willingness to commit volume in exchange for pricing stability and feature roadmap access."
                ),
                test=(
                    "Pilot a 2-year committed-volume contract structure with 20 enterprise accounts up for "
                    "renewal in Q3 2026; track signed ACV vs. prior run-rate and net take-rate impact."
                ),
            ),
        ],
        sources=[
            Source(
                id=1,
                title="Stripe Expands Financial Services Suite With New Issuing and Treasury Features",
                publisher="TechCrunch",
                published_at="2026-04-08T10:00:00Z",
                url="https://techcrunch.com/2026/04/08/stripe-financial-services-expansion",
            ),
            Source(
                id=2,
                title="Stripe Launches Stablecoin Financial Accounts in 101 Countries",
                publisher="The Block",
                published_at="2026-04-22T14:00:00Z",
                url="https://theblock.co/2026/04/22/stripe-stablecoin-accounts",
            ),
            Source(
                id=3,
                title="Stripe Tax Now Available in 50 Countries Following EMEA Expansion",
                publisher="Business Wire",
                published_at="2026-04-15T09:30:00Z",
                url="https://businesswire.com/2026/04/15/stripe-tax-expansion",
            ),
            Source(
                id=4,
                title="How AI Synthetic Identity Fraud Is Testing Payments Infrastructure",
                publisher="Financial Times",
                published_at="2026-04-29T07:00:00Z",
                url="https://ft.com/content/stripe-fraud-ai-2026",
            ),
            Source(
                id=5,
                title="Stripe Acquires Lemon Squeezy to Deepen Merchant-of-Record Play",
                publisher="Reuters",
                published_at="2026-05-01T11:00:00Z",
                url="https://reuters.com/technology/stripe-lemon-squeezy-acquisition",
            ),
            Source(
                id=6,
                title="Stripe Files Confidentially for IPO at $91.5 Billion Valuation",
                publisher="Wall Street Journal",
                published_at="2026-05-05T06:00:00Z",
                url="https://wsj.com/articles/stripe-ipo-filing-2026",
            ),
        ],
        generated_at=datetime.now(timezone.utc).isoformat(),
        confidence_caveats=(
            "This brief is based on publicly available news and analyst commentary from April–May 2026. "
            "TPV, revenue, and valuation figures are sourced from press reports and have not been independently "
            "verified against audited financials. Stripe remains a private company; all financial data is "
            "estimated or reported by third parties. Treat as directional context for meeting preparation only."
        ),
    )

import json

INSIGHT_REPORT_SCHEMA = {
    "company": "string",
    "executive_summary": "string — 3-5 sentence overview of the company's current strategic position",
    "investment_thesis": "string — 2-3 sentence PE investment thesis",
    "bull_case": ["string — specific upside driver (3-5 items)"],
    "bear_case": ["string — specific risk or headwind (3-5 items)"],
    "strategic_themes": [
        {
            "theme": "string — theme name",
            "evidence": "string — specific evidence from the articles",
            "sources": ["integer — 1-based index into the sources array"],
        }
    ],
    "risk_flags": [
        {
            "category": "string — e.g. Regulatory, Competitive, Macro, Operational",
            "severity": "string — High | Medium | Low",
            "rationale": "string — specific rationale grounded in article evidence",
            "sources": ["integer — 1-based index into the sources array"],
        }
    ],
    "value_creation_hypotheses": [
        {
            "lever": "string — e.g. Pricing power, Sales efficiency, M&A",
            "hypothesis": "string — specific testable hypothesis",
            "evidence": "string — evidence from articles or peer benchmarks",
            "test": "string — concrete 30-90 day experiment or measurement",
        }
    ],
    "sources": [
        {
            "id": "integer — 1-based, matches indices used in sources arrays above",
            "title": "string",
            "publisher": "string",
            "published_at": "string — ISO 8601",
            "url": "string",
        }
    ],
    "generated_at": "string — ISO 8601 UTC timestamp",
    "confidence_caveats": "string — honest statement of data limitations",
}

_STRIPE_EXAMPLE_ARTICLES = [
    {
        "title": "Stripe Launches Stablecoin Financial Accounts in 101 Countries",
        "source": "The Block",
        "published_at": "2026-04-22T14:00:00Z",
        "snippet": (
            "Stripe has launched Stablecoin Financial Accounts, enabling businesses in 101 countries "
            "to hold and transact in USDC and USDB, leveraging its $1.1B Bridge acquisition."
        ),
        "url": "https://theblock.co/2026/04/22/stripe-stablecoin-accounts",
    },
    {
        "title": "Stripe Files Confidentially for IPO at $91.5 Billion Valuation",
        "source": "Wall Street Journal",
        "published_at": "2026-05-05T06:00:00Z",
        "snippet": (
            "Stripe has filed confidentially with the SEC for an IPO at a reported valuation of $91.5B, "
            "below its 2021 peak of $95B, as the company targets a public listing later this year."
        ),
        "url": "https://wsj.com/articles/stripe-ipo-filing-2026",
    },
    {
        "title": "Stripe Acquires Lemon Squeezy to Deepen Merchant-of-Record Play",
        "source": "Reuters",
        "published_at": "2026-05-01T11:00:00Z",
        "snippet": (
            "Stripe has acquired Lemon Squeezy, a Merchant of Record platform popular with indie SaaS "
            "developers, extending its reach into the long-tail creator and micro-SaaS segment."
        ),
        "url": "https://reuters.com/technology/stripe-lemon-squeezy-acquisition",
    },
]

_STRIPE_EXAMPLE_OUTPUT = {
    "company": "Stripe",
    "executive_summary": (
        "Stripe enters 2026 as the dominant payments infrastructure layer for the internet economy, "
        "processing over $1 trillion in annualised TPV across 50+ countries. Recent product moves — "
        "Stablecoin Financial Accounts and the acquisition of Lemon Squeezy — signal an intentional "
        "pivot from pure payments rail to full-stack financial operating system. The company filed "
        "confidentially for an IPO at $91.5B, reflecting a more defensible revenue-quality story "
        "than its 2021 peak valuation."
    ),
    "investment_thesis": (
        "Stripe is the canonical payments-to-platform compounder with sticky infrastructure, "
        "network effects on both sides of the merchant-developer market, and a credible path to "
        "capturing bank-grade margin through stablecoin rails and embedded finance products."
    ),
    "bull_case": [
        "Stablecoin Financial Accounts in 101 countries could disintermediate cross-border wire fees, "
        "a multi-billion dollar TAM currently captured by correspondent banking networks.",
        "Lemon Squeezy acquisition extends reach into high-LTV, low-churn creator and micro-SaaS segment.",
        "IPO filing crystallises a liquidity path while the balance sheet remains strong for further M&A.",
    ],
    "bear_case": [
        "IPO at $91.5B demands sustained growth in a rate-sensitive environment; any revenue slip risks "
        "multiple compression for public-market investors.",
        "Regulatory fragmentation across 101 stablecoin jurisdictions creates compliance overhead that "
        "scales non-linearly with geographic expansion.",
        "Take-rate compression from enterprise negotiations continues to pressure blended margins.",
    ],
    "strategic_themes": [
        {
            "theme": "Stablecoin infrastructure buildout",
            "evidence": (
                "Stripe launched Stablecoin Financial Accounts in 101 countries, directly leveraging "
                "the $1.1B Bridge acquisition as its orchestration layer."
            ),
            "sources": [1],
        },
        {
            "theme": "SMB and creator economy expansion",
            "evidence": (
                "Acquisition of Lemon Squeezy targets the indie SaaS and creator segment, a cohort "
                "with high LTV and low churn that complements Stripe's enterprise motion."
            ),
            "sources": [3],
        },
    ],
    "risk_flags": [
        {
            "category": "Valuation / IPO execution",
            "severity": "High",
            "rationale": (
                "A confidential filing at $91.5B — below the 2021 peak — requires sustaining growth "
                "momentum. Any deceleration could trigger a down-round dynamic damaging to employee "
                "morale and secondary liquidity."
            ),
            "sources": [2],
        },
        {
            "category": "Regulatory",
            "severity": "Medium",
            "rationale": (
                "Operating stablecoin accounts across 101 jurisdictions exposes Stripe to divergent "
                "reserve, AML, and licensing requirements that could force costly product localisation."
            ),
            "sources": [1],
        },
    ],
    "value_creation_hypotheses": [
        {
            "lever": "Stablecoin cross-border take-rate",
            "hypothesis": (
                "Routing international B2B payables through the Bridge stablecoin rail at 0.5% undercuts "
                "SWIFT wire costs of 1.5-3%, capturing share while expanding Stripe's treasury margin."
            ),
            "evidence": "Bridge processed $5B in stablecoin volume in 2024 prior to acquisition.",
            "test": (
                "Enable stablecoin payout as default for eligible cross-border payouts in Latin America "
                "and Southeast Asia for one quarter; compare net take-rate to equivalent wire volume."
            ),
        },
    ],
    "sources": [
        {
            "id": 1,
            "title": "Stripe Launches Stablecoin Financial Accounts in 101 Countries",
            "publisher": "The Block",
            "published_at": "2026-04-22T14:00:00Z",
            "url": "https://theblock.co/2026/04/22/stripe-stablecoin-accounts",
        },
        {
            "id": 2,
            "title": "Stripe Files Confidentially for IPO at $91.5 Billion Valuation",
            "publisher": "Wall Street Journal",
            "published_at": "2026-05-05T06:00:00Z",
            "url": "https://wsj.com/articles/stripe-ipo-filing-2026",
        },
        {
            "id": 3,
            "title": "Stripe Acquires Lemon Squeezy to Deepen Merchant-of-Record Play",
            "publisher": "Reuters",
            "published_at": "2026-05-01T11:00:00Z",
            "url": "https://reuters.com/technology/stripe-lemon-squeezy-acquisition",
        },
    ],
    "generated_at": "2026-05-09T08:00:00Z",
    "confidence_caveats": (
        "This brief is based on publicly available news from April-May 2026. Stripe remains a private "
        "company; all financial figures are from press reports and have not been verified against "
        "audited financials. Treat as directional context for meeting preparation only."
    ),
}

_SYSTEM_PROMPT = """\
You are a senior Bain & Company analyst preparing pre-meeting intelligence briefs for PE partners.

YOUR ROLE:
- Synthesise recent news into a rigorous, PE-grade insight brief
- Ground every claim in the provided articles — do not hallucinate facts
- Cite sources using their 1-based index (e.g. sources: [1, 3])
- Write with precision and economy — no filler, no hedging beyond what the evidence supports
- Severity for risk_flags must be one of: High, Medium, Low
- Do not include percentages in any user-facing text fields

OUTPUT FORMAT:
Respond with a single valid JSON object exactly matching this schema:
{schema}
""".format(
    schema=json.dumps(INSIGHT_REPORT_SCHEMA, indent=2)
)

_ONE_SHOT_USER = """\
ARTICLES (3 total):

[1] {a1_title} ({a1_source}, {a1_date})
{a1_snippet}
URL: {a1_url}

[2] {a2_title} ({a2_source}, {a2_date})
{a2_snippet}
URL: {a2_url}

[3] {a3_title} ({a3_source}, {a3_date})
{a3_snippet}
URL: {a3_url}

Company: Stripe
Generate the insight report JSON.\
""".format(
    a1_title=_STRIPE_EXAMPLE_ARTICLES[0]["title"],
    a1_source=_STRIPE_EXAMPLE_ARTICLES[0]["source"],
    a1_date=_STRIPE_EXAMPLE_ARTICLES[0]["published_at"],
    a1_snippet=_STRIPE_EXAMPLE_ARTICLES[0]["snippet"],
    a1_url=_STRIPE_EXAMPLE_ARTICLES[0]["url"],
    a2_title=_STRIPE_EXAMPLE_ARTICLES[1]["title"],
    a2_source=_STRIPE_EXAMPLE_ARTICLES[1]["source"],
    a2_date=_STRIPE_EXAMPLE_ARTICLES[1]["published_at"],
    a2_snippet=_STRIPE_EXAMPLE_ARTICLES[1]["snippet"],
    a2_url=_STRIPE_EXAMPLE_ARTICLES[1]["url"],
    a3_title=_STRIPE_EXAMPLE_ARTICLES[2]["title"],
    a3_source=_STRIPE_EXAMPLE_ARTICLES[2]["source"],
    a3_date=_STRIPE_EXAMPLE_ARTICLES[2]["published_at"],
    a3_snippet=_STRIPE_EXAMPLE_ARTICLES[2]["snippet"],
    a3_url=_STRIPE_EXAMPLE_ARTICLES[2]["url"],
)

_ONE_SHOT_ASSISTANT = json.dumps(_STRIPE_EXAMPLE_OUTPUT, indent=2)


def build_prompt(articles: list[dict], company: str) -> str:
    article_block = "\n\n".join(
        f"[{i + 1}] {a['title']} ({a['source']}, {a['published_at']})\n{a['snippet']}\nURL: {a['url']}"
        for i, a in enumerate(articles)
    )
    user_turn = (
        f"ARTICLES ({len(articles)} total):\n\n"
        f"{article_block}\n\n"
        f"Company: {company}\n"
        f"Generate the insight report JSON."
    )
    return "\n\n".join([_SYSTEM_PROMPT, _ONE_SHOT_USER, _ONE_SHOT_ASSISTANT, user_turn])

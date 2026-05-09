from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

# ─── Shared fixtures ──────────────────────────────────────────────────────────

SAMPLE_ARTICLES = [
    {
        "title": "Stripe Reports Record Enterprise Bookings",
        "url": "https://example.com/stripe-bookings",
        "published_at": "2026-05-01T00:00:00Z",
        "snippet": "Stripe posted record enterprise bookings in Q1 2026.",
        "source": "Reuters",
    }
]

VALID_REPORT_DICT = {
    "company": "Stripe",
    "executive_summary": "Stripe is the dominant payments infrastructure layer for the internet economy.",
    "investment_thesis": "A sticky platform compounder with expanding financial services attach rate.",
    "bull_case": ["Enterprise bookings accelerating."],
    "bear_case": ["Take-rate compression risk."],
    "strategic_themes": [
        {"theme": "Platform expansion", "evidence": "11 product lines beyond core payments.", "sources": [1]}
    ],
    "risk_flags": [
        {"category": "Competitive", "severity": "High", "rationale": "Adyen closing the gap.", "sources": [1]}
    ],
    "value_creation_hypotheses": [
        {
            "lever": "Financial services attach rate",
            "hypothesis": "Cross-selling Issuing to Capital users grows ARPU.",
            "evidence": "Multi-product merchants retain at a higher rate.",
            "test": "Run 90-day cross-sell pilot for Capital users.",
        }
    ],
    "sources": [
        {
            "id": 1,
            "title": "Stripe Reports Record Enterprise Bookings",
            "publisher": "Reuters",
            "published_at": "2026-05-01T00:00:00Z",
            "url": "https://example.com/stripe-bookings",
        }
    ],
    "generated_at": "2026-05-09T08:00:00Z",
    "confidence_caveats": "Based on publicly available news only.",
}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# ─── /health ──────────────────────────────────────────────────────────────────


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ─── /api/insights — pipeline ─────────────────────────────────────────────────


def test_insights_returns_200_with_valid_pipeline(client):
    with patch("app.main.fetch_all_news", new=AsyncMock(return_value=SAMPLE_ARTICLES)), \
         patch("app.main.synthesize", new=AsyncMock(return_value=VALID_REPORT_DICT)):
        response = client.post("/api/insights", json={"company": "Stripe"})

    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "Stripe"
    assert "executive_summary" in data
    assert "bull_case" in data
    assert "risk_flags" in data


def test_insights_response_matches_insight_report_schema(client):
    with patch("app.main.fetch_all_news", new=AsyncMock(return_value=SAMPLE_ARTICLES)), \
         patch("app.main.synthesize", new=AsyncMock(return_value=VALID_REPORT_DICT)):
        response = client.post("/api/insights", json={"company": "Stripe"})

    data = response.json()
    # Verify all top-level schema fields are present
    expected_fields = {
        "company", "executive_summary", "investment_thesis",
        "bull_case", "bear_case", "strategic_themes", "risk_flags",
        "value_creation_hypotheses", "sources", "generated_at", "confidence_caveats",
    }
    assert expected_fields.issubset(data.keys())


def test_insights_returns_503_when_no_articles_found(client):
    with patch("app.main.fetch_all_news", new=AsyncMock(return_value=[])):
        response = client.post("/api/insights", json={"company": "ObscureCorp99"})

    assert response.status_code == 503
    assert "detail" in response.json()


def test_insights_returns_422_for_missing_company_field(client):
    response = client.post("/api/insights", json={})
    assert response.status_code == 422


# ─── /api/insights — cache ────────────────────────────────────────────────────


def test_insights_cache_miss_calls_fetch_and_synthesize(client):
    fetch_mock = AsyncMock(return_value=SAMPLE_ARTICLES)
    synth_mock = AsyncMock(return_value=VALID_REPORT_DICT)

    with patch("app.main.fetch_all_news", fetch_mock), \
         patch("app.main.synthesize", synth_mock):
        response = client.post("/api/insights", json={"company": "Stripe"})

    assert response.status_code == 200
    fetch_mock.assert_awaited_once_with("Stripe")
    synth_mock.assert_awaited_once()


def test_insights_cache_hit_skips_fetch_and_synthesize(client):
    fetch_mock = AsyncMock(return_value=SAMPLE_ARTICLES)
    synth_mock = AsyncMock(return_value=VALID_REPORT_DICT)

    with patch("app.main.fetch_all_news", fetch_mock), \
         patch("app.main.synthesize", synth_mock):
        # First request — cache miss
        r1 = client.post("/api/insights", json={"company": "Stripe"})
        # Second request — cache hit
        r2 = client.post("/api/insights", json={"company": "Stripe"})

    assert r1.status_code == 200
    assert r2.status_code == 200
    # Pipeline called exactly once despite two requests
    assert fetch_mock.await_count == 1
    assert synth_mock.await_count == 1


def test_insights_cache_is_case_insensitive(client):
    fetch_mock = AsyncMock(return_value=SAMPLE_ARTICLES)
    synth_mock = AsyncMock(return_value=VALID_REPORT_DICT)

    with patch("app.main.fetch_all_news", fetch_mock), \
         patch("app.main.synthesize", synth_mock):
        client.post("/api/insights", json={"company": "Stripe"})
        client.post("/api/insights", json={"company": "STRIPE"})
        client.post("/api/insights", json={"company": "stripe"})

    # All three map to the same cache key — pipeline only runs once
    assert fetch_mock.await_count == 1
    assert synth_mock.await_count == 1


def test_insights_cache_is_isolated_per_company(client):
    fetch_mock = AsyncMock(return_value=SAMPLE_ARTICLES)
    synth_mock = AsyncMock(return_value=VALID_REPORT_DICT)

    with patch("app.main.fetch_all_news", fetch_mock), \
         patch("app.main.synthesize", synth_mock):
        client.post("/api/insights", json={"company": "Stripe"})
        client.post("/api/insights", json={"company": "Shopify"})

    # Different companies — pipeline runs independently for each
    assert fetch_mock.await_count == 2
    assert synth_mock.await_count == 2

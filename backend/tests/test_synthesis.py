import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import ValidationError

from app.models import InsightReport
from app.services.llm import synthesize, synthesize_with_gemini, synthesize_with_groq

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
    "bull_case": ["Enterprise bookings accelerating.", "Stablecoin rails capturing cross-border TAM."],
    "bear_case": ["Take-rate compression from enterprise negotiations.", "Regulatory fragmentation risk."],
    "strategic_themes": [
        {"theme": "Platform expansion", "evidence": "11 product lines beyond core payments.", "sources": [1]}
    ],
    "risk_flags": [
        {"category": "Competitive", "severity": "High", "rationale": "Adyen closing developer-experience gap.", "sources": [1]}
    ],
    "value_creation_hypotheses": [
        {
            "lever": "Financial services attach rate",
            "hypothesis": "Cross-selling Issuing to Capital users grows ARPU without incremental CAC.",
            "evidence": "Multi-product merchants retain at a higher rate than single-product users.",
            "test": "Run 90-day cross-sell pilot for Capital users with material processing volume.",
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
    "confidence_caveats": "Based on publicly available news only. Not verified against audited financials.",
}


# ─── Gemini synthesis ─────────────────────────────────────────────────────────


async def test_synthesize_with_gemini_returns_parsed_dict():
    mock_response = MagicMock()
    mock_response.text = json.dumps(VALID_REPORT_DICT)

    mock_client = MagicMock()
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    with patch("app.services.llm.create_gemini_client", return_value=mock_client):
        result = await synthesize_with_gemini(SAMPLE_ARTICLES, "Stripe")

    assert isinstance(result, dict)
    assert result["company"] == "Stripe"
    assert "executive_summary" in result
    assert "bull_case" in result


async def test_synthesize_with_groq_returns_parsed_dict():
    mock_message = MagicMock()
    mock_message.content = json.dumps(VALID_REPORT_DICT)

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=mock_message)]

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("app.services.llm.create_groq_client", return_value=mock_client):
        result = await synthesize_with_groq(SAMPLE_ARTICLES, "Stripe")

    assert isinstance(result, dict)
    assert result["company"] == "Stripe"


# ─── Pydantic validation ──────────────────────────────────────────────────────


def test_insight_report_validation_passes_with_valid_dict():
    report = InsightReport(**VALID_REPORT_DICT)

    assert report.company == "Stripe"
    assert report.risk_flags[0].severity == "High"
    assert len(report.bull_case) == 2
    assert len(report.sources) == 1
    assert report.sources[0].id == 1


def test_insight_report_validation_fails_with_invalid_severity():
    invalid = {
        **VALID_REPORT_DICT,
        "risk_flags": [
            {"category": "Competitive", "severity": "CRITICAL", "rationale": "Bad.", "sources": [1]}
        ],
    }
    with pytest.raises(ValidationError) as exc_info:
        InsightReport(**invalid)

    assert "severity" in str(exc_info.value).lower()


def test_insight_report_validation_fails_with_missing_required_field():
    incomplete = {k: v for k, v in VALID_REPORT_DICT.items() if k != "executive_summary"}
    with pytest.raises(ValidationError):
        InsightReport(**incomplete)


def test_insight_report_validation_fails_with_wrong_source_type():
    invalid = {
        **VALID_REPORT_DICT,
        "sources": [
            {
                "id": "not-an-int",
                "title": "Some article",
                "publisher": "Reuters",
                "published_at": "2026-05-01T00:00:00Z",
                "url": "https://example.com/1",
            }
        ],
    }
    with pytest.raises(ValidationError):
        InsightReport(**invalid)


# ─── Retry and fallback behaviour ─────────────────────────────────────────────


async def test_synthesize_falls_back_to_groq_on_gemini_exception():
    """Any non-rate-limit Gemini failure should fall through to Groq."""
    mock_message = MagicMock()
    mock_message.content = json.dumps(VALID_REPORT_DICT)
    mock_groq_response = MagicMock()
    mock_groq_response.choices = [MagicMock(message=mock_message)]
    mock_groq_client = MagicMock()
    mock_groq_client.chat.completions.create = AsyncMock(return_value=mock_groq_response)

    with patch(
        "app.services.llm._synthesize_gemini_with_backoff",
        side_effect=RuntimeError("Gemini unavailable"),
    ), patch("app.services.llm.create_groq_client", return_value=mock_groq_client):
        result = await synthesize(SAMPLE_ARTICLES, "Stripe")

    assert result["company"] == "Stripe"


async def test_synthesize_falls_back_to_groq_on_rate_limit():
    """A 429 rate-limit error should bypass tenacity retries and go straight to Groq."""
    mock_message = MagicMock()
    mock_message.content = json.dumps(VALID_REPORT_DICT)
    mock_groq_response = MagicMock()
    mock_groq_response.choices = [MagicMock(message=mock_message)]
    mock_groq_client = MagicMock()
    mock_groq_client.chat.completions.create = AsyncMock(return_value=mock_groq_response)

    with patch(
        "app.services.llm._synthesize_gemini_with_backoff",
        side_effect=Exception("429 Resource Exhausted — quota exceeded"),
    ), patch("app.services.llm.create_groq_client", return_value=mock_groq_client):
        result = await synthesize(SAMPLE_ARTICLES, "Stripe")

    assert result["company"] == "Stripe"


async def test_synthesize_gemini_validation_failure_triggers_groq_fallback():
    """
    If Gemini returns JSON that fails Pydantic validation, the caller (main.py)
    raises ValidationError. Here we verify synthesize itself surfaces a fallback
    when the underlying call raises — simulating a bad-schema response scenario.
    """
    mock_message = MagicMock()
    mock_message.content = json.dumps(VALID_REPORT_DICT)
    mock_groq_response = MagicMock()
    mock_groq_response.choices = [MagicMock(message=mock_message)]
    mock_groq_client = MagicMock()
    mock_groq_client.chat.completions.create = AsyncMock(return_value=mock_groq_response)

    with patch(
        "app.services.llm._synthesize_gemini_with_backoff",
        side_effect=ValueError("invalid JSON returned by Gemini"),
    ), patch("app.services.llm.create_groq_client", return_value=mock_groq_client):
        result = await synthesize(SAMPLE_ARTICLES, "Stripe")

    assert isinstance(result, dict)
    assert result["company"] == "Stripe"

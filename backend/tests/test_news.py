from unittest.mock import AsyncMock, patch

import pytest

from app.services.news import fetch_all_news, fetch_gnews, fetch_newsapi

# ─── Raw API payloads (as returned by each provider before normalization) ─────

_GNEWS_RAW = {
    "title": "Stripe IPO Filing Confirmed",
    "url": "https://example.com/stripe-ipo",
    "publishedAt": "2026-05-05T06:00:00Z",
    "description": "Stripe has filed confidentially for an IPO.",
    "source": {"name": "Wall Street Journal"},
}

_NEWSAPI_RAW = {
    "title": "Stripe Stablecoin Launch",
    "url": "https://example.com/stripe-stablecoin",
    "publishedAt": "2026-04-22T14:00:00Z",
    "description": "Stripe launches stablecoin accounts.",
    "source": {"name": "The Block"},
}


# ─── fetch_gnews ──────────────────────────────────────────────────────────────


async def test_fetch_gnews_normalizes_article_fields():
    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = [_GNEWS_RAW]
        articles = await fetch_gnews("Stripe")

    assert len(articles) == 1
    a = articles[0]
    assert a["title"] == "Stripe IPO Filing Confirmed"
    assert a["url"] == "https://example.com/stripe-ipo"
    assert a["published_at"] == "2026-05-05T06:00:00Z"
    assert a["snippet"] == "Stripe has filed confidentially for an IPO."
    assert a["source"] == "Wall Street Journal"


async def test_fetch_gnews_returns_empty_when_key_missing():
    with patch("app.services.news.settings") as mock_settings:
        mock_settings.gnews_api_key = None
        articles = await fetch_gnews("Stripe")

    assert articles == []


async def test_fetch_gnews_returns_empty_on_http_error():
    import httpx

    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as mock_call:
        mock_call.side_effect = httpx.RequestError("connection timeout")
        articles = await fetch_gnews("Stripe")

    assert articles == []


# ─── fetch_newsapi ────────────────────────────────────────────────────────────


async def test_fetch_newsapi_normalizes_article_fields():
    with patch("app.services.news._call_newsapi", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = [_NEWSAPI_RAW]
        articles = await fetch_newsapi("Stripe")

    assert len(articles) == 1
    a = articles[0]
    assert a["title"] == "Stripe Stablecoin Launch"
    assert a["source"] == "The Block"
    assert a["published_at"] == "2026-04-22T14:00:00Z"


async def test_fetch_newsapi_returns_empty_when_key_missing():
    with patch("app.services.news.settings") as mock_settings:
        mock_settings.newsapi_key = None
        articles = await fetch_newsapi("Stripe")

    assert articles == []


# ─── fetch_all_news ───────────────────────────────────────────────────────────


async def test_fetch_all_news_deduplicates_same_url():
    """
    GNews and NewsAPI both return the same story — one with a trailing slash.
    _url_hash strips it before hashing, so only one article should survive.
    """
    duplicate = {**_GNEWS_RAW, "url": "https://example.com/stripe-ipo/"}

    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as gnews_mock, \
         patch("app.services.news._call_newsapi", new_callable=AsyncMock) as newsapi_mock:
        gnews_mock.return_value = [_GNEWS_RAW]
        newsapi_mock.return_value = [duplicate]
        articles = await fetch_all_news("Stripe")

    assert len(articles) == 1


async def test_fetch_all_news_deduplicates_case_insensitive_url():
    upper_url = {**_GNEWS_RAW, "url": "HTTPS://EXAMPLE.COM/STRIPE-IPO"}

    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as gnews_mock, \
         patch("app.services.news._call_newsapi", new_callable=AsyncMock) as newsapi_mock:
        gnews_mock.return_value = [_GNEWS_RAW]
        newsapi_mock.return_value = [upper_url]
        articles = await fetch_all_news("Stripe")

    assert len(articles) == 1


async def test_fetch_all_news_sorts_by_published_at_descending():
    older = {**_GNEWS_RAW, "publishedAt": "2026-04-01T00:00:00Z", "url": "https://example.com/old"}
    newer = {**_NEWSAPI_RAW, "publishedAt": "2026-05-10T00:00:00Z", "url": "https://example.com/new"}

    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as gnews_mock, \
         patch("app.services.news._call_newsapi", new_callable=AsyncMock) as newsapi_mock:
        gnews_mock.return_value = [older]
        newsapi_mock.return_value = [newer]
        articles = await fetch_all_news("Stripe")

    assert articles[0]["published_at"] == "2026-05-10T00:00:00Z"
    assert articles[1]["published_at"] == "2026-04-01T00:00:00Z"


async def test_fetch_all_news_caps_results_at_15():
    raw_articles = [
        {**_GNEWS_RAW, "url": f"https://example.com/article-{i}", "publishedAt": f"2026-05-{i:02d}T00:00:00Z"}
        for i in range(1, 21)
    ]

    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as gnews_mock, \
         patch("app.services.news._call_newsapi", new_callable=AsyncMock) as newsapi_mock:
        gnews_mock.return_value = raw_articles
        newsapi_mock.return_value = []
        articles = await fetch_all_news("Stripe")

    assert len(articles) == 15


async def test_fetch_all_news_returns_empty_when_both_sources_empty():
    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as gnews_mock, \
         patch("app.services.news._call_newsapi", new_callable=AsyncMock) as newsapi_mock:
        gnews_mock.return_value = []
        newsapi_mock.return_value = []
        articles = await fetch_all_news("UnknownCorp")

    assert articles == []


async def test_fetch_all_news_partial_source_failure_returns_available_articles():
    """One source failing should not suppress results from the other."""
    import httpx

    with patch("app.services.news._call_gnews_api", new_callable=AsyncMock) as gnews_mock, \
         patch("app.services.news._call_newsapi", new_callable=AsyncMock) as newsapi_mock:
        gnews_mock.side_effect = httpx.RequestError("timeout")
        newsapi_mock.return_value = [_NEWSAPI_RAW]
        articles = await fetch_all_news("Stripe")

    assert len(articles) == 1
    assert articles[0]["source"] == "The Block"

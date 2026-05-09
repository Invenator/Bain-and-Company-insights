import asyncio
import hashlib
import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

GNEWS_BASE_URL = "https://gnews.io/api/v4/search"
NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"


async def _call_gnews_api(client: httpx.AsyncClient, company: str) -> list[dict]:
    response = await client.get(
        GNEWS_BASE_URL,
        params={
            "q": company,
            "lang": "en",
            "max": 10,
            "sortby": "publishedAt",
            "apikey": settings.gnews_api_key,
        },
    )
    response.raise_for_status()
    return response.json().get("articles", [])


async def fetch_gnews(company: str) -> list[dict]:
    if not settings.gnews_api_key:
        logger.warning("GNEWS_API_KEY is not set — skipping GNews fetch")
        return []

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            raw_articles = await _call_gnews_api(client, company)
    except httpx.HTTPStatusError as exc:
        logger.warning(
            "GNews request failed with status %s: %s",
            exc.response.status_code,
            exc.response.text[:200],
        )
        return []
    except httpx.RequestError as exc:
        logger.warning("GNews request error (%s): %s", type(exc).__name__, exc)
        return []

    return [
        {
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "snippet": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
        }
        for article in raw_articles
    ]


async def _call_newsapi(client: httpx.AsyncClient, company: str) -> list[dict]:
    response = await client.get(
        NEWSAPI_BASE_URL,
        params={
            "q": company,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 10,
            "apiKey": settings.newsapi_key,
        },
    )
    response.raise_for_status()
    return response.json().get("articles", [])


async def fetch_newsapi(company: str) -> list[dict]:
    if not settings.newsapi_key:
        logger.warning("NEWSAPI_KEY is not set — skipping NewsAPI fetch")
        return []

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            raw_articles = await _call_newsapi(client, company)
    except httpx.HTTPStatusError as exc:
        logger.warning(
            "NewsAPI request failed with status %s: %s",
            exc.response.status_code,
            exc.response.text[:200],
        )
        return []
    except httpx.RequestError as exc:
        logger.warning("NewsAPI request error (%s): %s", type(exc).__name__, exc)
        return []

    return [
        {
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "snippet": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
        }
        for article in raw_articles
    ]


def _url_hash(url: str) -> str:
    normalized = url.strip().rstrip("/").lower()
    return hashlib.md5(normalized.encode()).hexdigest()


async def fetch_all_news(company: str) -> list[dict]:
    gnews_articles, newsapi_articles = await asyncio.gather(
        fetch_gnews(company),
        fetch_newsapi(company),
    )

    if not gnews_articles and not newsapi_articles:
        logger.warning("All news sources returned empty results for company: %s", company)

    seen_hashes: set[str] = set()
    unique_articles: list[dict] = []

    for article in gnews_articles + newsapi_articles:
        url_hash = _url_hash(article["url"])
        if url_hash not in seen_hashes:
            seen_hashes.add(url_hash)
            unique_articles.append(article)

    unique_articles.sort(key=lambda a: a["published_at"], reverse=True)

    return unique_articles[:15]

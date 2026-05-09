import json
import logging

from google import genai
from google.genai import types
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from app.config import settings
from app.models import InsightReport
from app.services.synthesis import build_prompt

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"


def create_gemini_client() -> genai.Client:
    return genai.Client(api_key=settings.gemini_api_key)


def create_groq_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def _is_rate_limit_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "429" in msg or "rate limit" in msg or "quota" in msg or "resource_exhausted" in msg


async def synthesize_with_gemini(articles: list[dict], company: str) -> dict:
    client = create_gemini_client()
    prompt = build_prompt(articles, company)

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InsightReport,
        ),
    )
    return json.loads(response.text)


async def synthesize_with_groq(articles: list[dict], company: str) -> dict:
    client = create_groq_client()
    prompt = build_prompt(articles, company)

    response = await client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception(lambda exc: not _is_rate_limit_error(exc)),
    reraise=True,
)
async def _synthesize_gemini_with_backoff(articles: list[dict], company: str) -> dict:
    return await synthesize_with_gemini(articles, company)


async def synthesize(articles: list[dict], company: str) -> dict:
    try:
        return await _synthesize_gemini_with_backoff(articles, company)
    except Exception as exc:
        if _is_rate_limit_error(exc):
            logger.warning("Gemini rate limit hit — falling back to Groq immediately")
        else:
            logger.warning("Gemini failed after retries (%s) — falling back to Groq", exc)
        return await synthesize_with_groq(articles, company)

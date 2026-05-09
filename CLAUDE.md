# Project: Bain Company Intelligence Tool

## Purpose
FastAPI + React PoC that fetches recent news for a company and synthesizes
it into a PE-grade insight brief using Gemini 2.5 Flash.

## Stack
- Backend: Python 3.12, FastAPI, httpx, pydantic-settings, google-genai, groq, tenacity, cachetools
- Frontend: React 18, TypeScript, Vite, Tailwind CSS
- Testing: pytest + pytest-asyncio (backend), Vitest + RTL (frontend)
- Linting: ruff (Python), ESLint + Prettier (TypeScript)

## Architecture Rules
- All news API calls are server-side only. Never expose API keys to the frontend.
- NewsAPI.org must never be called from React — CORS is blocked on free tier.
- No LangChain. No abstraction frameworks. Direct SDK calls only.
- No vector DB. Direct in-context summarization with Gemini 2.5 Flash.
- Gemini primary, Groq Llama 3.3 70B failover. Same OpenAI-compatible code path.

## Code Style
- Python: ruff-compliant, type hints on all functions, async def for all I/O
- TypeScript: strict mode, named exports, no `any`
- Variable names: descriptive — `article_list`, `insight_report`, never `x`, `d`, `res`
- No inline comments explaining what the code does. Comments explain why.

## Commit Format (conventional commits)
feat(scope): description
fix(scope): description
chore(scope): description
docs(scope): description

## Design Tokens (Bain brand)
Primary navy: #003478
Accent red: #CC0000
Background: #F5F5F5
Border: #E0E0E0
Font: Inter
Border radius: 4px

## What NOT to Do
- No LangChain
- No Redis (use cachetools.TTLCache)
- No percentages in any user-facing text
- No spinner loading states — use skeleton screens
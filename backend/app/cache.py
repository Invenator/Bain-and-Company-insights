from cachetools import TTLCache

_TTL_SECONDS = 86_400  # 24 hours

_cache: TTLCache = TTLCache(maxsize=128, ttl=_TTL_SECONDS)


def get_cached_report(company: str) -> dict | None:
    return _cache.get(company.lower())


def set_cached_report(company: str, report: dict) -> None:
    _cache[company.lower()] = report

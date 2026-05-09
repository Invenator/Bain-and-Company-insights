import os
import sys
from pathlib import Path

# Must be set before any app.* import — Settings() validates at module load time.
os.environ.setdefault("GNEWS_API_KEY", "test-gnews-key")
os.environ.setdefault("NEWSAPI_KEY", "test-newsapi-key")
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("GROQ_API_KEY", "test-groq-key")

# Make `import app.*` resolve to backend/app/.
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def clear_cache():
    from app.cache import _cache

    _cache.clear()
    yield
    _cache.clear()

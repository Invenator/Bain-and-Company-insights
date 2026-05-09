from pydantic import model_validator
from pydantic_settings import BaseSettings

REQUIRED_KEYS = ("gnews_api_key", "newsapi_key", "gemini_api_key", "groq_api_key")


class Settings(BaseSettings):
    gnews_api_key: str | None = None
    newsapi_key: str | None = None
    gemini_api_key: str | None = None
    groq_api_key: str | None = None

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @model_validator(mode="after")
    def check_required_keys(self) -> "Settings":
        missing = [key for key in REQUIRED_KEYS if not getattr(self, key)]
        if missing:
            env_vars = ", ".join(key.upper() for key in missing)
            raise ValueError(f"Missing required environment variables: {env_vars}")
        return self


settings = Settings()

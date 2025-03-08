from contextvars import ContextVar
from functools import lru_cache
import logging
from pathlib import Path
from typing import Optional

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from schemas.bot import BotParseMode

SRC_PATH = Path(__file__).parent.parent.resolve()

_REQUEST_ID: ContextVar = ContextVar("request_id", default=None)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SRC_PATH.joinpath(".env"), extra="ignore"
    )

    @property
    def src_path(self) -> Path:
        return SRC_PATH

    @property
    def request_id(self) -> Optional[str]:
        return _REQUEST_ID.get()

    @request_id.setter
    def request_id(self, value: Optional[str]) -> None:
        _REQUEST_ID.set(value)

    # === Sentry ===

    sentry_dsn: Optional[str] = Field(None, alias="SENTRY_DSN")
    sentry_sample_rate: float = Field(1.0, alias="SENTRY_SAMPLE_RATE")
    sentry_enable_tracing: bool = Field(True, alias="SENTRY_ENABLE_TRACING")
    sentry_traces_sample_rate: float = Field(0.2, alias="SENTRY_TRACES_SAMPLE_RATE")

    # === Logging ===

    log_level: int | str = Field(logging.INFO, alias="LOG_LEVEL")

    # === App ===

    app_name: str = Field("MyBot", alias="APP_NAME")
    app_description: str = Field("My awesome bot 🚀", alias="APP_DESCRIPTION")
    app_version: str = Field("0.1.0", alias="APP_VERSION")
    app_host: str = Field("localhost", alias="APP_HOST")
    app_port: int = Field(8000, alias="APP_PORT")
    app_url_path_prefix: str = Field("/v1/mybot", alias="APP_URL_PATH_PREFIX")

    @property
    def app_keyprefix(self) -> str:
        return self.app_name.upper()

    @property
    def app_openapi_url(self) -> str:
        return f"{self.app_url_path_prefix}/openapi.json"

    @property
    def app_docs_url(self) -> str:
        return f"{self.app_url_path_prefix}/docs"

    @property
    def app_redoc_url(self) -> str:
        return f"{self.app_url_path_prefix}/redoc"

    # === Bot ===

    bot_token: str = Field(..., alias="BOT_TOKEN")
    bot_parse_mode: str = Field(BotParseMode.HTML.value, alias="BOT_PARSE_MODE")
    webhook_base_url: HttpUrl = Field(..., alias="WEBHOOK_BASE_URL")
    webhook_sert_pub: Optional[Path] = Field(None, alias="WEBHOOK_SERT_PUB")
    webhook_secret: Optional[str] = Field(None, alias="WEBHOOK_SECRET")
    webhook_url_path: str = Field("/callbacks/telegram/mybot", alias="WEBHOOK_URL_PATH")

    @property
    def webhook_url(self) -> str:
        return (
            self.webhook_base_url.unicode_string().rstrip("/")
            + self.webhook_url_path
        )

    # === Redis ===

    redis_db: int = Field(0, alias="REDIS_DB")
    redis_user: str = Field("", alias="REDIS_USER")
    redis_pswd: str = Field("", alias="REDIS_PSWD")
    redis_host: str = Field("localhost", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_decode_responses: bool = Field(True, alias="REDIS_DECODE_RESPONSES")
    redis_retries: int = Field(3, alias="REDIS_RETRIES")

    @property
    def redis_dsn(self) -> str:
        return (
            f"redis://{self.redis_user}:{self.redis_pswd}"
            f"@{self.redis_host}:{self.redis_port}"
            f"/{self.redis_db}"
        )

    # === Postgres ===

    postgres_db: str = Field("postgres", alias="POSTGRES_DB")
    postgres_user: str = Field("postgres", alias="POSTGRES_USER")
    postgres_pswd: str = Field("postgres", alias="POSTGRES_PSWD")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_pswd}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()

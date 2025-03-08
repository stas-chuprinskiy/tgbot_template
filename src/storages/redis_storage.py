from functools import lru_cache
from typing import Any

from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError

from core.config import get_settings


class RedisStorage(Redis):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def _get_keyprefixed_key(self, key: str) -> str:
        return f"{get_settings().app_keyprefix}_{key}"

    # === Do your stuff here ===

    ...


@lru_cache
def get_redis_storage() -> RedisStorage:
    return RedisStorage.from_url(
        url=get_settings().redis_dsn,
        decode_responses=get_settings().redis_decode_responses,
        retry=Retry(
            backoff=ExponentialBackoff(), retries=get_settings().redis_retries
        ),
        retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
    )

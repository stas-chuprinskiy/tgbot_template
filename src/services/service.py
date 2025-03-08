from functools import lru_cache
from typing import Any

from storages.pg_storage import get_pg_storage
from storages.redis_storage import get_redis_storage


class Service:
    _instance = None

    pg_storage = get_pg_storage()
    redis_storage = get_redis_storage()

    def __init__(self) -> None:
        ...

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    # === Do your stuff here ===

    ...


@lru_cache
def get_service() -> Service:
    return Service()

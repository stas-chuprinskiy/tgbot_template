from functools import lru_cache
from typing import Any

from loguru import logger
from telebot.async_telebot import AsyncTeleBot, ExceptionHandler
from telebot.storage import StateRedisStorage

from core.config import get_settings


class CustomExceptionHandler(ExceptionHandler):  # type: ignore
    async def handle(self, exception: Exception) -> bool:
        logger.exception(exception)
        return True


class CustomAsyncTeleBot(AsyncTeleBot):  # type: ignore
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance


@lru_cache
def get_bot() -> CustomAsyncTeleBot:
    return CustomAsyncTeleBot(
        token=get_settings().bot_token,
        parse_mode=get_settings().bot_parse_mode,
        exception_handler=CustomExceptionHandler(),
        state_storage=StateRedisStorage(
            prefix=get_settings().app_keyprefix,
            redis_url=get_settings().redis_dsn,
        ),
    )


async def setup_bot_webhook() -> None:
    webhook_info = await get_bot().get_webhook_info()
    if webhook_info.url != get_settings().webhook_url:
        await get_bot().remove_webhook()

        webhook_params = {"url": get_settings().webhook_url}
        if get_settings().webhook_sert_pub:
            with open(get_settings().webhook_sert_pub, "r") as f:
                cert = f.read()
            webhook_params["certificate"] = cert
        if get_settings().webhook_secret:
            webhook_params["secret_token"] = get_settings().webhook_secret

        await get_bot().set_webhook(**webhook_params)

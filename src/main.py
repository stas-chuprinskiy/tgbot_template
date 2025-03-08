# ruff: noqa: E402

import asyncio
from http import HTTPStatus
import uvloop
import uuid

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Awaitable, Callable

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger
from telebot.types import Update
import uvicorn

from bot.bot import get_bot, setup_bot_webhook
from core.config import get_settings
from core.loggers import init_loguru
from core.sentry import init_sentry
from storages.pg_storage import get_pg_storage
from storages.redis_storage import get_redis_storage


# === Sentry and Loguru ===


init_sentry()

init_loguru()


# === Init app ===


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await setup_bot_webhook()

    yield

    await get_pg_storage().close()
    await get_redis_storage().aclose()


app = FastAPI(lifespan=lifespan)


# === Middlewares ===


@app.middleware("http")
async def log_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("X-Request-ID")
    if request_id is None:
        request_id = str(uuid.uuid4())

    get_settings().request_id = request_id

    forwarded_for = request.headers.get("x-forwarded-for")
    real_ip = request.headers.get("x-real-ip")

    client_ip = None
    if forwarded_for:
        client_ip = forwarded_for.strip().split(",")[0].strip()
    elif real_ip:
        client_ip = real_ip.strip()
    else:
        client_ip = request.client.host if request.client else client_ip

    user_agent = request.headers.get("user-agent", None)

    with logger.contextualize(request_id=request_id):
        logger.info(
            f"⏩ Request  [{request_id}] {request.method} {request.url.path} | "
            f"IP: {client_ip} | User-Agent: {user_agent}"
        )

        response = await call_next(request)

        logger.info(
            f"⏪ Response [{request_id}] {request.method} {request.url.path} | "
            f"Status: {response.status_code}"
        )

        return response


# === Webhook ===


@app.post(get_settings().webhook_url_path, include_in_schema=False)
async def process_webhook(request: Request) -> Response:
    webhook_secret_header_name = "X-Telegram-Bot-Api-Secret-Token"
    secret_header = request.headers.get(webhook_secret_header_name)
    if get_settings().webhook_secret and secret_header != get_settings().webhook_secret:
        logger.warning(
            "Incorrect secret header, update forbidden"
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await get_bot().process_new_updates([Update.de_json(await request.json())])

    return Response(status_code=status.HTTP_200_OK)


# === Error handling ===


@app.exception_handler(Exception)
async def error_handler(_: Request, e: Exception) -> JSONResponse:
    logger.exception(
        f"❌ Error {e.__class__.__name__} [{get_settings().request_id}]: {e}"
    )

    return JSONResponse(
        content=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
    )


# === Entrypoint ===


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=get_settings().app_host,
        port=get_settings().app_port,
        reload=True,
    )

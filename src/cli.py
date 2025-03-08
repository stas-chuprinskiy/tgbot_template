# ruff: noqa: E402

import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import typer

from core.loggers import init_loguru
from services.service import get_service  # noqa: F401

init_loguru()

app = typer.Typer()


@app.command()
def foo() -> None:
    # === Do your stuff here ===

    # asyncio.run(get_service().foo())

    ...


if __name__ == "__main__":
    app()

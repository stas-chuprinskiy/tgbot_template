import sys

from loguru import logger

from core.config import get_settings

LOG_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

STDOUT_LOGGER = {
    "sink": sys.stdout,
    "level": get_settings().log_level,
    "colorize": True,
    "format": (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level: <8}"
        " | <level>{name}:{function}:{line} - {message}</level>"
    ),
}


def init_loguru() -> None:
    logger.remove()
    logger.add(**STDOUT_LOGGER)  # type: ignore

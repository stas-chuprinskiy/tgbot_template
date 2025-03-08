from core.config import get_settings

import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration


def init_sentry() -> None:
    if get_settings().sentry_dsn:
        sentry_sdk.init(
            dsn=get_settings().sentry_dsn,
            integrations=[LoguruIntegration()],
            sample_rate=get_settings().sentry_sample_rate,
            enable_tracing=get_settings().sentry_enable_tracing,
            traces_sample_rate=get_settings().sentry_traces_sample_rate,
        )

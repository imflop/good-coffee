import typing as t

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import Middleware

from ..api.v1.health import router as health
from ..api.v1.hook import router as hooks
from .settings import LOGGER_KEY, SETTINGS_KEY, AppSettings

API_PREFIX = "/api/v1"


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(health, prefix=f"{API_PREFIX}/check", tags=["health"])
    # app.include_router(info, prefix=f"{API_PREFIX}/check", tags=["info"])
    app.include_router(hooks, prefix=f"{API_PREFIX}/hooks", tags=["hooks"])
    return app


def add_origins() -> t.Sequence[str]:
    return ("http://localhost:9000", "http://0.0.0.0:9000", "http://api:9000")


def setup_app(settings: AppSettings) -> FastAPI:
    logger = settings.configure_logging()

    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_hosts or add_origins(),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    if settings.sentry_dsn and not settings.debug:
        sentry_sdk.init(dsn=settings.sentry_dsn, release="0.0.1")
        middlewares.append(Middleware(SentryAsgiMiddleware))

    app = FastAPI(
        title="good_coffee_near_me",
        version="0.0.1",
        description="Good coffee",
        middleware=middlewares,
        default_response_class=ORJSONResponse,
        **{SETTINGS_KEY: settings, LOGGER_KEY: logger},  # type: ignore
    )

    app = register_routers(app)

    return app

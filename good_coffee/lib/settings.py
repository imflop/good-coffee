import logging
import sys
import typing as t

import loguru
from loguru import logger
from pydantic import BaseSettings, Field, PostgresDsn

from .loggers import InterceptHandler

SETTINGS_KEY: str = "settings"
LOGGER_KEY: str = "loguru_logger"


class BaseAppSettings(BaseSettings):
    class Config:
        env_file = ".env"


class AppSettings(BaseAppSettings):
    debug: bool = Field(True, env="debug", help="Debug flag")
    host: str = Field("0.0.0.0", env="host", help="Hostname to run webserver")
    port: int = Field(9000, env="port", help="Webservers port")
    sentry_dsn: t.Optional[str] = Field(None, env="sentry_dsn", help="Sentry DSN")

    database_dsn: PostgresDsn = Field(
        ...,
        env="database_dsn",
        help="Database DSN",
    )
    max_connection_count: int = 10
    min_connection_count: int = 10

    telegram_api_token: str = Field(..., env="telegram_api_token", help="Bot token")
    secret_key: str = "super-secret-key"

    allowed_hosts: t.Sequence[str] = ["*"]
    logging_level: int = logging.INFO  # type: ignore
    loggers: t.Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    def configure_logging(self) -> "loguru.Logger":
        logging.getLogger().handlers = [InterceptHandler()]  # type: ignore

        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)  # type: ignore
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])

        return logger

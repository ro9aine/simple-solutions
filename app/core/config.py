from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/deribit",
        alias="DATABASE_URL",
    )
    celery_broker_url: str = Field(default="memory://", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(
        default="cache+memory://",
        alias="CELERY_RESULT_BACKEND",
    )
    deribit_base_url: str = Field(
        default="https://www.deribit.com/api/v2",
        alias="DERIBIT_BASE_URL",
    )
    default_tickers: list[str] = Field(
        default=["BTC_USD", "ETH_USD"],
        alias="DEFAULT_TICKERS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("default_tickers", mode="before")
    @classmethod
    def parse_default_tickers(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip().upper() for item in value.split(",") if item.strip()]
        return [item.upper() for item in value]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

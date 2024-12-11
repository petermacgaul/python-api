import os
from functools import lru_cache
from typing import Type

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "API"
    DB_URL: str = Field(validation_alias="DATABASE_URL")
    DB_FORCE_ROLLBACK: bool = False
    DB_ARGUMENTS: dict[str, str | bool] = {}
    ENCRYPT_KEY: str = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="
    JWT_KEY: str = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="
    DEBUG: bool = False
    TESTING: bool = False


class ProductionSettings(Settings):
    pass


class StagingSettings(Settings):
    DEVELOPMENT: bool = True
    DEBUG: bool = True


class DevelopmentSettings(Settings):
    DEVELOPMENT: bool = True
    DEBUG: bool = True


class TestingSettings(Settings):
    TESTING: bool = True
    DB_URL: str = "sqlite+aiosqlite:///:memory:"
    DB_FORCE_ROLLBACK: bool = True
    DB_ARGUMENTS: dict[str, str | bool] = {"check_same_thread": False}

    __test__ = False  # Prevent pytest from discovering this class as a test class


config_environments: dict[str, Type[Settings]] = {
    "PRODUCTION": ProductionSettings,
    "DEVELOPMENT": DevelopmentSettings,
    "TESTING": TestingSettings,
    "STAGING": StagingSettings,
}


@lru_cache()
def get_settings() -> Settings:
    return config_environments[os.environ["ENVIRONMENT"]]()


settings = get_settings()

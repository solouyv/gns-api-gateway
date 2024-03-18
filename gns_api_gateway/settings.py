from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    env: str = "development"
    version: str = "1.0"

    logger_level: str = Field("INFO", env="LOG_LEVEL")

    documentation_enabled: bool = True

    gns3_url: str

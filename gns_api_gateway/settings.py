from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db: str

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    env: str = "development"
    version: str = "1.0"
    logger_level: str = Field("INFO", env="LOG_LEVEL")
    documentation_enabled: bool = True
    gns3_url: str
    database: DatabaseSettings = DatabaseSettings()

    gns3_server_url: str

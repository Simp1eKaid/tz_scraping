from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """Основная конфигурация приложения"""

    # Настройки приложения
    APP_NAME: str = "Books Scraper API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Настройки парсера
    REQUEST_TIMEOUT: int = 20
    CONCURRENT_REQUESTS: int = 10

    # Логирование
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Кэширование 
    CACHE_TTL: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
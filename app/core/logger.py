from loguru import logger
import sys
from app.core.config import settings

def setup_logger():
    """Настройка loguru"""

    # Удаляем стандартный обработчик
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True,
        enqueue=True  # безопасно для async
    )

    # Можно добавить запись в файл (опционально)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        enqueue=True
    )

    logger.info(f"Logger initialized with level: {settings.LOG_LEVEL}")

setup_logger()
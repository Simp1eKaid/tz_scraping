from pydantic import BaseModel, Field
from typing import List, Optional

class BookItem(BaseModel):
    """Модель одной книги"""
    title: str = Field(..., description="Название книги")
    price: float = Field(..., description="Цена книги")
    rating: int = Field(..., ge=1, le=5, description="Руйтинг от 1 до 5")
    in_stock: bool = Field(..., description="Наличие книги")

class SceapePageResponse(BaseModel):
    status: str = Field(..., description="success или error")
    page_url: str
    count: int
    items: List[BookItem]
    error: Optional[str] = Field(None, description="Сообщение об ошибке, если status=error")

class MultiScrapeResponse(BaseModel):
    """Ответ для множественного парсинга"""
    status: str = "success"
    total_count: int
    page_count: int
    execution_time: float = Field(..., description="Время выполнения в секундах")
    results: List[ScrapePageResponse]

class HelthResponse(BaseModel):
    """Health check"""
    status: str = "ok"


class ErrorResponse(BaseModel):
    """Error Model"""
    status: str = "error"
    detail: str


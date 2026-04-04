# app/schemas/response.py
from pydantic import BaseModel, Field
from typing import List, Optional


class BookItem(BaseModel):
    """Модель одной книги"""
    title: str
    price: float
    rating: int = Field(..., ge=1, le=5)
    in_stock: bool


class ScrapePageResponse(BaseModel):
    """Ответ для одной страницы"""
    status: str
    page_url: str
    count: int
    items: List[BookItem]
    error: Optional[str] = None


class MultiScrapeResponse(BaseModel):
    """Ответ для множественного парсинга"""
    status: str = "success"
    total_count: int
    page_count: int
    execution_time: float
    results: List[ScrapePageResponse]


class HealthResponse(BaseModel):
    """Health-check"""
    status: str = "ok"


class ErrorResponse(BaseModel):
    """Модель ошибки"""
    status: str = "error"
    detail: str
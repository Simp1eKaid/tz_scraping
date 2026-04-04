from fastapi import APIRouter, Query, HTTPException, Request
from pydantic import HttpUrl
from typing import List
import time
import asyncio

from app.parsers.books import scrape_single_page, scrape_multiple_pages
from app.schemas.response import (
    ScrapePageResponse,
    MultiScrapeResponse,
    HealthResponse,
    ErrorResponse,
    BookItem
)

router = APIRouter(prefix="/api/v1", tags=["scrape"])


@router.get("/scrape", response_model=ScrapePageResponse)
async def scrape_page(
    url: str = Query(..., description="URL страницы каталога books.toscrape.com")
):
    """
    Парсинг одной страницы каталога.
    Пример: /api/v1/scrape?url=https://books.toscrape.com/catalogue/page-2.html
    """
    # Проверка, что URL принадлежит нужному сайту
    if not url.startswith("https://books.toscrape.com"):
        raise HTTPException(
            status_code=422,
            detail="URL должен принадлежать books.toscrape.com"
        )
    
    try:
        result = await scrape_single_page(url)
        
        # Если парсер вернул ошибку
        if result.get("status") == "error":
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch page: {result.get('error', 'Unknown error')}"
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal parsing error: {str(e)}"
        )
    
@router.post("/scrape/multi", response_model=MultiScrapeResponse)
async def scrape_multi(urls: List[str]):
    """
    Параллельный парсинг нескольких страниц.
    Принимает список URL в теле запроса.
    """
    if not urls:
        raise HTTPException(status_code=400, detail="URL список не может быть пустым")

    # Проверка всех URL
    for url in urls:
        if not url.startswith("https://books.toscrape.com"):
            raise HTTPException(
                status_code=422,
                detail="Все URLs должны принадлежать books.toscrape.com"
            )
    # Замеряем время
    start_time = time.time()
    
    try:
        page_results = await scrape_multiple_pages(urls)
        
        total_count = sum(page.get("count", 0) for page in page_results)
        
        return {
            "status": "success",
            "total_count": total_count,
            "page_count": len(urls),
            "execution_time": round(time.time() - start_time, 2),
            "results": page_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multi-page parsing error: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Простой health-check эндпоинт"""
    return {"status": "ok"}
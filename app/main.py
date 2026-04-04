# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers.scrape import router as scrape_router

app = FastAPI(
    title="Books.toScrape Parser API",
    description="REST API для парсинга книг с books.toscrape.com",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем CORS (чтобы можно было тестировать из браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем наши роутеры
app.include_router(scrape_router)


@app.get("/")
async def root():
    return {
        "message": "Books Scraper API is running",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
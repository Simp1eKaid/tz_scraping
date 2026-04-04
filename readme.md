# Books.toScrape Parser API

REST API сервис для асинхронного парсинга интернет-магазина книг [books.toscrape.com](https://books.toscrape.com).

## Стек технологий

- **Python 3.12**
- FastAPI
- aiohttp + BeautifulSoup4
- Pydantic v2 + pydantic-settings
- Loguru (структурированное логирование)
- Docker + Docker Compose

## Быстрый запуск

### 1. Через Docker Compose (рекомендуемый способ)

```bash
# Клонируем репозиторий
git clone https://github.com/Simp1eKaid/tz_scraping.git
cd tz_scraping

# Запуск одной командой
docker compose up --build -d

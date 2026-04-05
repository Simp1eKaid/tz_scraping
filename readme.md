# Books.toScrape Parser API

REST API сервис для асинхронного парсинга интернет-магазина книг [books.toscrape.com](https://books.toscrape.com).

## Стек технологий

- **Python 3.12**
- FastAPI
- aiohttp + BeautifulSoup4
- Pydantic v2 + pydantic-settings
- Loguru (структурированное логирование)
- Docker + Docker Compose

## Основные возможности

- Парсинг одной страницы каталога
- Параллельный парсинг нескольких страниц (`/multi`)
- Валидация URL (только `books.toscrape.com`)
- Корректная обработка ошибок (400, 422, 502, 500)
- Health-check эндпоинт
- Запуск от непривилегированного пользователя в Docker
- Логирование

## Быстрый запуск

### 1. Через Docker Compose (рекомендуемый способ)

```bash
# Клонируем репозиторий
git clone https://github.com/Simp1eKaid/tz_scraping.git
cd tz_scraping
```
создать .env файл, пример: .env.exampl
```bash
# Запуск одной командой
docker compose up --build -d
```
Приложение будет доступно по адресу: http://localhost:8000

### 2. Локальный запуск (для разработки)
```bash
# Создаём виртуальное окружение
python -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запуск
python -m app.main
```
# API Endpoints
Метод,Эндпоинт,Описание
GET,/api/v1/health,Health check
GET,/api/v1/scrape,Парсинг одной страницы
POST,/api/v1/scrape/multi,Параллельный парсинг нескольких страниц

# Примеры запросов
Парсинг одной страницы:
```bash
curl "http://localhost:8000/api/v1/scrape?url=https://books.toscrape.com/catalogue/page-2.html"
```
Параллельный парсинг:
```bash
curl -X POST "http://localhost:8000/api/v1/scrape/multi" \
  -H "Content-Type: application/json" \
  -d '["https://books.toscrape.com/catalogue/page-1.html", "https://books.toscrape.com/catalogue/page-2.html"]'
```

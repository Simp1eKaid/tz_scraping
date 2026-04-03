import asyncio
from typing import Dict, List, Optional
import aiohttp
from bs4 import BeautifulSoup, Tag
from loguru import logger

class BookParser:
    """Парсер карточек с сайта"""
    BASE_URL = "https://books.toscrape.com"

    @staticmethod
    def _parse_rating(rating_class: str) -> int:
        """Преобразует класс рейтинга (One, Two, Three...) в число 1-5"""
        rating_map = {
            "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
        }
        for word, value in rating_map.items():
            if word in rating_class:
                return value
        return 0
    
    @staticmethod
    def parse_book(article: Tag) -> Optional[Dict]:
        try:
            # Title
            title_tag = article.find("h3").find("a") if article.find("h3") else None
            title = title_tag.get("title") or title_tag.get_text(strip=True) if title_tag else "Unknown Title"

            # Price
            price_tag = article.find("p", class_="price_color")
            price_str = price_tag.get_text(strip=True) if price_tag else "0.00"
            price = float(price_str.replace("£", "").replace("Â£", ""))

            # Rating
            rating_tag = article.find("p", class_="star-rating")
            rating_class = rating_tag.get("class") if rating_tag else []
            rating = BookParser._parse_rating(" ".join(rating_class))

            # In_stock
            availability_tag = article.find("p", class_="instock")
            in_stock = False
            if availability_tag:
                text = availability_tag.get_text(strip=True).lower()
                in_stock = "in stock" in text

            return {
                "title": title,
                "price": round(price, 2),
                "rating": rating,
                "in_stock": in_stock,
            }

        except Exception as e:
            logger.warning(f"Failed to parse book card: {e}")
            return None
        
    @staticmethod
    async def scrape_page(url: str, session: aiohttp.ClientSession) -> Dict:
        """
        Асинхронно загружает страницу и парсит все книги на ней.
        Возвращает словарь с результатами для одной страницы.
        """
        try:
            async with session.get(url, timeout=15) as response:
                if response.status != 200:
                    logger.error(f"HTTP {response.status} for {url}")
                    return {
                        "page_url": url,
                        "status": "error",
                        "error": f"HTTP {response.status}",
                        "items": [],
                        "count": 0
                    }

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Находим все карточки книг
                articles: List[Tag] = soup.find_all("article", class_="product_pod")

                items = []
                for article in articles:
                    book = BookParser.parse_book(article)
                    if book:
                        items.append(book)

                logger.info(f"Successfully parsed {len(items)} books from {url}")

                return {
                    "page_url": url,
                    "status": "success",
                    "count": len(items),
                    "items": items
                }

        except asyncio.TimeoutError:
            logger.error(f"Timeout while fetching {url}")
            return {
                "page_url": url,
                "status": "error",
                "error": "Request timeout",
                "items": [],
                "count": 0
            }
        except Exception as e:
            logger.exception(f"Unexpected error parsing {url}")
            return {
                "page_url": url,
                "status": "error",
                "error": str(e),
                "items": [],
                "count": 0
            }


# Удобная функция для использования в роутерах
async def scrape_single_page(url: str) -> Dict:
    """Обёртка для парсинга одной страницы"""
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        return await BookParser.scrape_page(url, session)


async def scrape_multiple_pages(urls: List[str]) -> List[Dict]:
    """Параллельный парсинг нескольких страниц"""
    timeout = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
    async with timeout as session:
        tasks = [BookParser.scrape_page(url, session) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Обрабатываем возможные исключения в gather
        processed = []
        for result in results:
            if isinstance(result, Exception):
                processed.append({
                    "status": "error",
                    "error": str(result),
                    "items": [],
                    "count": 0
                })
            else:
                processed.append(result)

        return processed
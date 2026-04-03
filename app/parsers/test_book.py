# test_parser.py
import asyncio
from app.parsers.books import scrape_single_page

async def main():
    url = "https://books.toscrape.com/catalogue/page-2.html"
    
    print(f"Запускаем парсинг страницы: {url}")
    result = await scrape_single_page(url)
    
    print(f"\nСтатус: {result['status']}")
    print(f"Найдено книг: {result['count']}")
    print(f"URL страницы: {result['page_url']}")
    
    if result['items']:
        print("\nПример первой книги:")
        book = result['items'][0]
        print(f"   Название: {book['title']}")
        print(f"   Цена:     £{book['price']}")
        print(f"   Рейтинг:  {book['rating']} из 5")
        print(f"   В наличии: {book['in_stock']}")
        
        print(f"\nВсего книг на странице: {len(result['items'])}")

if __name__ == "__main__":
    asyncio.run(main())
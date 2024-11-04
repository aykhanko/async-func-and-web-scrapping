import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import time

s = time.time()
books_database = {}

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return await response.text()

async def categories():
    url = "https://books.toscrape.com/index.html"
    await_text = await fetch(url)
    soup = BeautifulSoup(await_text, "html.parser")
    categories_link = soup.find_all("a")
    categories_list = [i.get_text(strip = True) for i in categories_link]
    return categories_list[3:]

async def categories_link():
    url = "https://books.toscrape.com/index.html"   
    await_text =  await fetch(url)
    soup = BeautifulSoup(await_text, "html.parser")
    categories_link = soup.find_all("a")
    categories_list = [url[:27]+i["href"] for i in categories_link if i["href"][:25] == "catalogue/category/books/"]
    return categories_list


async def books_data(url):
    await_text = await fetch(url)
    soup = BeautifulSoup(await_text, "html.parser")

    book_name = soup.find_all("h3")
    book_price = soup.find_all("p", class_ = "price_color")

    books_list = []
    for count, (b, p) in enumerate(zip(book_name, book_price) ,start = 1):
        book_data = {
            "Book": b.find("a").get("title"),
            "Price": p.text[2:] + " GPB"
        }
        books_list.append(book_data)
    print(f"{count} book info saved")
    return books_list

async def main():
    categories_list = await categories()
    links = await categories_link()

    for category, link in zip(categories_list, links):
        books_database[category] = await books_data(link)
    with open ("booktoscrape.json", "w") as f:
        f.write(json.dumps(books_database, indent=4, ensure_ascii=False))

asyncio.run(main())
e = time.time()
print(e-s)

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
import json

s = time.time()
quote_database = {}

async def await_text(url,session):
    response = await session.get(url)
    return await response.text()
    
async def data():
    async with aiohttp.client.ClientSession() as session:
        tasks = []
    
        for page in range(1,11):
            url = f"https://quotes.toscrape.com/page/{page}/"
            tasks.append(await_text(url,session))

        pages_info = await asyncio.gather(*tasks)
           
        for page_number, content in enumerate(pages_info, start=1):
            soup = BeautifulSoup(content, "html.parser")
            authors = soup.find_all("small", class_="author")
            texts = soup.find_all("span", class_="text")
            quote_database[f"Page {page_number}"] = []

            for author, text in zip(authors,texts):
                quote_database[f"Page {page_number}"].append({
                    "Auhtor": author.text,
                    "Text": text.text
                }) 
                
    print(json.dumps(quote_database, indent=4, ensure_ascii=False))

asyncio.run(data())
e = time.time()
print(e-s)
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import json

globalnews_database = {}

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return await response.text()

async def news_links():
    url = "https://globalnews.ca/"
    links = []
    await_text = await fetch(url)
    soup = BeautifulSoup(await_text, "html.parser")
    news = soup.find_all("a", class_ = "c-posts__inner")
    for i in news:
        href = i.get("href")
        if href and href.startswith("https://globalnews.ca/news/"):
            links.append(href)
    
    return links

async def news(url):
    await_text = await fetch(url)
    soup = BeautifulSoup(await_text, "html.parser")

    news_title = soup.find("h1", class_ = "l-article__title") 
    news_text = soup.find("article", class_ = "l-article__text js-story-text") 
    news_date = soup.find("div", class_ = "c-byline__date c-byline__date--pubDate") 

    return {"Title" : news_title.text.strip() if news_title else "None",
            "Text" : news_text.text.strip() if news_text else "None",
            "Date" : news_date.text.strip() if news_date else "None"}
    
async def main():
    links = await news_links()
    tasks = []
    for count, link in enumerate(links, start =1):
        print(f"{count} data saved")
        tasks.append(news(link))

    results = await asyncio.gather(*tasks)
    
    for l, result in zip(links,results):
        globalnews_database[l] = result

    with open ("globalnews.json" , "w", encoding="utf8") as f:
        f.write(json.dumps(globalnews_database, indent=4, ensure_ascii=False))
    

asyncio.run(main())

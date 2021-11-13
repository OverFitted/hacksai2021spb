import aiohttp, asyncio
from bs4 import BeautifulSoup
import json
import time

TJ = "https://journal.tinkoff.ru"
TJ_search = "https://journal.tinkoff.ru/search/"


async def parse_urls(key_word):
    async with aiohttp.ClientSession() as session:
        async with session.get(TJ_search, params={
            "q": key_word,
        }) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            urls = [TJ + x.find("a")["href"] for x in soup.find_all("h2", {"class": "serp-item__title"})]
            return urls


async def get_text(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            text = " ".join(map(lambda x: x.text.strip().replace('\xa0', ''),
                                soup.find("div", {"class": "article-body"}).find_all("p")))
            return text


async def get_all_texts(keyword):
    urls = await parse_urls(keyword)
    all_texts = []
    for u in urls[:25]:
        text = await get_text(u)
        all_texts.append(text)
    return all_texts


async def tj_get_data(keyword, result_file_path='result-tj.json'):
    texts = await get_all_texts(keyword)
    result_dict = {"company": keyword,
                   "texts": texts}
    result_json = json.loads(json.dumps(result_dict))
    return result_json
    #with open(result_file_path, 'w', encoding='utf-8') as f:
        #json.dump(result_json, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tj_get_data("сбер", "sber-tj.json"))

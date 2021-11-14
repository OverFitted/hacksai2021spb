import requests
import re
import datetime
from bs4 import BeautifulSoup
import pandas as pd

C_NEWS = "https://cnews.ru/search"


def get_links_with_dates(keyword):
    r = requests.get(C_NEWS, params={"search": keyword})
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = list(map(lambda x: 'https:' + x["href"], soup.find_all("a", {"class": "ani-postname"})))
    dates = [x.text for x in soup.find_all("span", {"class": "ani-date"})]
    return urls, dates


def get_text(url):
    r = requests.get(url)
    text = ""
    try:
        news_soup = BeautifulSoup(r.text, 'html.parser').find("article")
        ps = news_soup.find_all("p")
        for p in ps:
            text += p.text.strip()
    except Exception as e:
        print(url)
    text = text.replace("\n", " ")
    return text


def get_all_texts_with_dates(keyword):
    urls, dates = get_links_with_dates(keyword)
    all_texts = []
    for u in range(len(urls)):
        if (not "https://softline" in urls[u]) and (not "https://events" in urls[u]):
            text = get_text(urls[u]).strip()
            date = dates[u]
            one_article = {'date': date, 'text': text}
            all_texts.append(one_article)
    return all_texts


if __name__ == "__main__":
    with open("input.txt", "r", encoding='utf-8') as f:
        file = f.readlines()
    for i in file:
        print(get_all_texts_with_dates(i.strip()))

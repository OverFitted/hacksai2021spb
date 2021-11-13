import requests
import re
import datetime
from bs4 import BeautifulSoup
import pandas as pd

C_NEWS = "https://cnews.ru/search"


def get_links(keyword):
    r = requests.get(C_NEWS, params={"search": keyword})
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = list(map(lambda x: 'https:' + x["href"], soup.find_all("a", {"class": "ani-postname"})))
    return urls


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


def get_all_texts(keyword):
    urls = get_links(keyword)
    all_texts = []
    for u in urls:
        if (not "https://softline" in u) and (not "https://events" in u):
            text = get_text(u).strip()
            all_texts.append(text)
    return all_texts


if __name__ == "__main__":
    with open("input.txt", "r", encoding='utf-8') as f:
        file = f.readlines()
    for i in file:
        print(get_all_texts(i.strip()))

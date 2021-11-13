import requests
import time
import json

from bs4 import BeautifulSoup

HABR_ROOT = "https://habr.com"
HABR_SEARCH = "https://habr.com/ru/search/"


def get_texts_urls(key_word, order='date'):
    page_number = 1
    all_urls = []
    max_urls = 50

    while page_number < max_urls:
        page = f'page{page_number}/'
        habr_search_url = HABR_SEARCH + page
        r = requests.get(habr_search_url, params={
            "q": key_word,
            "target_type": 'posts',
            "order": order
        })
        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        article_links_a_tags = soup.find_all("a", {"class": "tm-article-snippet__title-link"})
        for a in article_links_a_tags:
            article_url = a["href"]
            all_urls.append(HABR_ROOT + article_url)
        page_number += 1
    return all_urls


def parse_article_text(url):
    text = ""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    p_list = soup.find_all("p")
    for p in p_list:
        text += (p.text.strip()) if len(p.text) >= 20 else ''

    return text


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def get_all_texts_about_company(name):
    all_texts = []
    urls = get_texts_urls(name)
    for url in urls:
        text = parse_article_text(url)
        all_texts.append(text)

    return all_texts


def get_company_info(company_name, order='relevance'):
    rate = 0.0
    subscribers_str = ""
    subscribers_quantity = 0
    description = ""
    industries = []
    resp_search = requests.get(HABR_SEARCH, params={
        "q": company_name,
        "target_type": 'companies',
        "order": order
    })
    soup_search = BeautifulSoup(resp_search.text, 'html.parser').find_all("div", {
        'class': "tm-search-companies__item tm-search-companies__item_inlined"})
    try:
        company_element = soup_search[0]
        profile_url = HABR_ROOT + company_element.find("a")["href"]
    except IndexError as e:
        if str(e) == 'list index out of range':
            return
        else:
            print(e)
            return

    rate = float(str(company_element.find_all("span")[0].text).split()[1])
    subscribers_str = str(company_element.find_all("span")[1].text).split()[1]
    subscribers_quantity = int(float(subscribers_str[:-1]) * 1000 if "K" in subscribers_str else subscribers_str)

    resp_comp_profile = requests.get(profile_url)
    soup_profile = BeautifulSoup(resp_comp_profile.text, 'html.parser')
    paragraphs = soup_profile.find_all("dl", {'class': 'tm-description-list tm-description-list_variant-base'})
    for p in paragraphs:
        if p.find("dt",
                  {'class': "tm-description-list__title tm-description-list__title_variant-base"}).text == "О компании":
            description = p.find("dd").text
        elif p.find("dt",
                    {'class': "tm-description-list__title tm-description-list__title_variant-base"}).text == "Отрасли":
            industries = [x.strip() for x in p.find("dd").text.strip().split('\n') if x.strip() != ""]

    return {
        'description': description,
        'industries': industries,
        'rate': rate,
        'subscribers_str': subscribers_str,
        'subscribers_quantity': subscribers_quantity
    }


def build_data_json(company_name, result_file_path='result.json'):
    result_dict = dict()
    company_info = get_company_info(company_name)
    articles = [x for x in get_all_texts_about_company(company_name) if len(x) >= 200]
    articles_quantity = len(articles)
    result_dict["company_info"] = company_info
    result_dict["articles_quantity"] = articles_quantity
    result_dict["articles"] = articles
    result_json = json.loads(json.dumps(result_dict))

    with open(result_file_path, 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=4)


start = time.time()

build_data_json('яндекс', result_file_path='habr_yandex.json')
yandex = time.time()

build_data_json('сбер', result_file_path='habr_sber.json')
sber = time.time()

build_data_json('газпром', result_file_path='habr_gazprom.json')
gazprom = time.time()

print("yandex time:", yandex - start)
print("sber time: ", sber - yandex)
print("gazprom time: ", gazprom - sber)

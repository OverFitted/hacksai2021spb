import time

import requests
from bs4 import BeautifulSoup

URL_ROOT = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
# https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=lenta.ru&morphology=on&page_number=1


def parse_gz(keyword):
    while True:
        r = requests.get(URL_ROOT, headers={'User-Agent': 'Mozilla/5.0'},
                         params={
                             "searchString": keyword,
                             "morphology": "on",
                             # "sortDirection": "false",
                             # "sortBy":"UPDATE_DATE",
                             # "search-filter": "Дате+размещения",
                             "recordsPerPage": '_100',
                             "publishDateFrom": "01.01.2020",
                             "applSubmissionCloseDateFrom": "01.01.2021"
                         },
                         timeout=10)
        if r.status_code == 200:
            break
        time.sleep(5)

    soup = BeautifulSoup(r.text, 'html.parser')

    numbers = soup.find_all("div", {'class': 'registry-entry__header-mid__number'})
    values = soup.find_all("div", {'class': 'price-block__value'})
    descriptions = soup.find_all("div", {"class": "registry-entry__body-value"})
    dates = soup.find_all("div", {"class": "data-block__value"})
    customers = soup.find_all("div", {"class": "registry-entry__body-href"})

    #print(len(numbers))
    #print(len(values))
    #print(len(descriptions))
    #print(len(dates))
    #print(customers)
    #print(len(customers))

    result_list = []

    for i in range(len(numbers)):
        cur_dict = {}
        cur_dict["id"] = int(numbers[i].text.strip()[2:])
        cur_dict["value"] = float(values[i].text.strip().replace('\xa0', '').replace(',', '.')[:-2])
        cur_dict["description"] = descriptions[i].text.strip()
        cur_dict["date"] = dates[i].text.strip()
        cur_dict["customer"] = customers[i].text.strip()
        result_list.append(cur_dict)

    '''ids = [x["id"] for x in result_list]
    values = [x["value"] for x in result_list]
    descs = [x["description"] for x in result_list]
    dates = [x["date"] for x in result_list]
    customers = [x["customer"] for x in result_list]
    
    df = pd.DataFrame({'id': ids, 'value': values, 'desc': descs, 'date': dates, "customer": customers})
    df.to_csv("sber.csv")
    print(df)'''

    return result_list


if __name__ == "__main__":
    print(parse_gz("сбер"))

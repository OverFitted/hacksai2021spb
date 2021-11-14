from goszakupki import *
from habr_parser import *
from tinkoff_journal import *
from vcru import *
from c_news import *
from threading import Thread
from tqdm import tqdm

import asyncio


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None: self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


async def make_full_company_report(keyword, company_people, company_nomination):
    threads = []

    threads.append(ThreadWithReturnValue(target=parse_gz, args=(keyword,)))
    threads.append(ThreadWithReturnValue(target=get_all_texts_with_dates, args=(keyword,)))
    threads.append(ThreadWithReturnValue(target=build_data_json, args=(keyword,)))

    threads[0].start()
    threads[1].start()
    threads[2].start()

    vcru = await vc_get_data(keyword)
    tinkoff = await tj_get_data(keyword)

    people_parsed = []
    for person in company_people:
        people_threads = []
        people_threads.append(ThreadWithReturnValue(target=get_all_texts_with_dates, args=(f"{keyword} {person}",)))
        people_threads.append(ThreadWithReturnValue(target=build_data_json, args=(f"{keyword} {person}", 20,)))

        people_threads[0].start()
        people_threads[1].start()

        people_cnews = people_threads[0].join()
        people_habr = people_threads[1].join()

        people_parsed.append({
            "cnews": people_cnews,
            "habr": people_habr
        })

    goszakupki = threads[0].join()
    cnews = threads[1].join()
    habr = threads[2].join()

    result_dict = {
        "company": {
            "goszakupki": goszakupki,
            "habr": habr,
            "vcru": vcru,
            "tinkoff_journal": tinkoff,
            "cnews": cnews
        },
        "people": people_parsed,
        "nomination": company_nomination
    }
    return result_dict

    # async with open(result_file_path, 'wb', encoding='utf-8') as f:
    # json.dump(result_json, f, ensure_ascii=False, indent=4)


async def main():
    with open("input.txt", encoding='utf-8') as inp:
        infos = [x.split(" - ") for x in inp.readlines()]
        companies = [x[0] for x in infos]
        people = [x[1:-1] for x in infos]
        nominations = [x[-1] for x in infos]

    final_dict = dict()

    for company_id in tqdm(range(len(companies))):
        company_name = companies[company_id].strip()
        people[company_id] = [x.strip() for x in people[company_id]]
        report = await make_full_company_report(company_name, people[company_id], nominations[company_id])
        final_dict[company_name] = report
    final_json = json.loads(json.dumps(final_dict))
    with open("data/dataset.json", 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

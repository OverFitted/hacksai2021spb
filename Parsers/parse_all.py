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


async def make_full_company_report(keyword):
    threads = []

    # print(f'{keyword} start')
    threads.append(ThreadWithReturnValue(target=parse_gz, args=(keyword,)))
    threads.append(ThreadWithReturnValue(target=get_all_texts, args=(keyword,)))
    threads.append(ThreadWithReturnValue(target=build_data_json, args=(keyword,)))

    threads[0].start()
    threads[1].start()
    threads[2].start()

    vcru = await vc_get_data(keyword)
    # print(f"{keyword} vc: done")
    tinkoff = await tj_get_data(keyword)
    # print(f"{keyword} tj: done")

    goszakupki = threads[0].join()
    # print(f'{keyword} goszakupki: done')
    cnews = threads[1].join()
    # print(f"{keyword} cnews: done")
    habr = threads[2].join()
    # print(f"{keyword} habr: done")

    result_dict = {
        "goszakupki": goszakupki,
        "habr": habr,
        "vcru": vcru,
        "tinkoff_journal": tinkoff,
        "cnews": cnews
    }
    return result_dict

    # async with open(result_file_path, 'wb', encoding='utf-8') as f:
    # json.dump(result_json, f, ensure_ascii=False, indent=4)


async def main():
    with open("input.txt", encoding='utf-8') as inp:
        companies = inp.readlines()

    final_dict = dict()

    for company_name in tqdm(companies):
        company_name = company_name.strip()
        report = await make_full_company_report(company_name)
        final_dict[company_name] = report
        # print(f"{company_name} report completed")
    final_json = json.loads(json.dumps(final_dict))
    print("Final json builded")
    with open("jsons/dataset.json", 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    print("All done! bye")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

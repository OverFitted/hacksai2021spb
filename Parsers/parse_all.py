from goszakupki import *
from habr_parser import *
from tinkoff_journal import *
from vcru import *
import asyncio


async def make_full_company_report(keyword):
    print(f'{keyword} start')
    goszakupki = parse_gz(keyword)
    print(f'{keyword} goszakupki: done')
    habr = build_data_json(keyword)
    print(f"{keyword} habr: done")
    vcru = await get_data(keyword)
    print(f"{keyword} vc: done")
    tinkoff = await get_data(keyword)
    print(f"{keyword} tj: done")

    result_dict = {
        "goszakupki": goszakupki,
        "habr": habr,
        "vcru": vcru,
        "tinkoff_journal": tinkoff
    }
    return result_dict

    # async with open(result_file_path, 'wb', encoding='utf-8') as f:
    # json.dump(result_json, f, ensure_ascii=False, indent=4)


async def main():
    with open("input.txt", encoding='utf-8') as inp:
        companies = inp.readlines()

    final_dict = dict()

    for company_name in companies:
        report = await make_full_company_report(company_name)
        final_dict[company_name] = report
        print(f"{company_name} report completed")
    final_json = json.loads(json.dumps(final_dict))
    print("final json builded")
    with open("dataset.json", 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    print("all done! bye")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

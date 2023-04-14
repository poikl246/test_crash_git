import asyncio
import time
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import requests

headers = {'Accept': '*/*', 'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/56.0.3051.52',
           'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}


data = {}


async def fetch_url_data(session, url, duraz, Namber):
    try:
        async with session.get(url, headers=headers) as response:
            resp = await response.text()
            print(Namber)
            soup = BeautifulSoup(resp, 'html.parser')

            tible = soup.find_all('table')


            tible1 = tible[0].find_all('tr')

            tible2 = tible[1].find_all('tr')
            # print(tible2)

            one =[]

            for tib2 in tible2[1:]:
                local = []

                dat = tib2.find_all('td')

                for tut in dat[2:]:
                    local.append(tut)

                if one == []:
                    one = local
                elif one != local:
                    # print("NEN")
                    return 0



            if tible1[4].find_all('td')[1].text == '—' and (tible1[8].find_all('td')[1].text == '1000') and (tible1[-9].find_all('td')[1].text == '1' or tible1[-9].find_all('td')[1].text == '2') and (float((tible1[-7].find_all('td')[1].text)[:-1]) >= 10 and float((tible1[-7].find_all('td')[1].text)[:-1]) <= 13) and (int(str(tible1[-4].find_all('td')[1].text).replace(' ', '')) >= 1000000):

                data[f"{Namber}"] = {
                    'Name': tible1[0].find_all('td')[1].text,
                    'ISIN': tible1[1].find_all('td')[1].text,
                    'Data stop': tible1[5].find_all('td')[1].text,
                    'listing': tible1[-9].find_all('td')[1].text,
                    'Doxodnost': tible1[-7].find_all('td')[1].text,
                    'Doxod': tible1[-4].find_all('td')[1].text,
                    'Duracia': tible1[-2].find_all('td')[1].text,
                    'duraz':duraz
                }



    except Exception as e:
        print(e)
    else:
        return resp
    return


async def fetch_async(url_lists):
    tasks = []


    async with ClientSession() as session:
        for url, duraz, Namber in url_lists:
            task = asyncio.ensure_future(fetch_url_data(session, url, duraz, Namber))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
    return responses


def main():
    urls_list = []
    url_out = []
    caunt = 0
    print('Начинаю сбор данных')
    for i in range(1, 30 + 1):
        url = f'https://smart-lab.ru/q/bonds/order_by_val_to_day/desc/page{i}/?mat_years_lt=2'

        req = requests.get(url, headers=headers)

        src = req.text
        # print(src)
        soup = BeautifulSoup(src, 'html.parser')
        # print(soup)

        url_list = soup.find('table').find_all('tr')


        for url_ in url_list[1:]:
            caunt += 1
            stok = url_.find_all('td')
            stok2 = []
            for klsne in stok:
                stok2.append(str(klsne))

            if stok2.count('<td></td>') <= 1 and stok[-5].text != '':
                url_out.append([f'https://smart-lab.ru{stok[2].find("a").get("href")}', stok[-5].text, caunt])

    print(url_out)
    # url_out = url_out


    time.sleep(1)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_async(url_out))
    loop.run_until_complete(future)


if __name__ == "__main__":
    main()
    print(data)
    ips = data.keys()
    sorted_ips = sorted(ips, key=lambda ip: data[ip]['Doxodnost'], reverse=True)
    print(sorted_ips)
    knsepgk = [data[ip] for ip in sorted_ips]

    print('\n\n\n\n\n\n\n\n\nИтоговый и сортированный список')

    # print(knsepgk)
    for i in range(len(sorted_ips)):
        print(sorted_ips[i], knsepgk[i])
    print()
    print('Просто закройте программу')
    input()

    # out_list = ['№', "N", 'Название', 'ISIN', 'Дата погашения', 'Уровень листинга', 'Доходность', 'Объем день, руб', 'Дюрация, дней', ]


 
print('Просто закройте программу')
input()

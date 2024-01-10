import asyncio
import aiohttp
import datetime

API_KEY = 'xxx'

start_dates = []
date1 = '2023-09-01'
date2 = '2023-10-05'
start = datetime.datetime.strptime(date1, '%Y-%m-%d')
end = datetime.datetime.strptime(date2, '%Y-%m-%d')
step = datetime.timedelta(days=7)
while start <= end:
    start_dates.append(start)
    start += step


async def fetch(session, url):
    async with session.get(url) as resp:
        # print(resp.status)
        return (await resp.json())['element_count']


async def collect():
    async with aiohttp.ClientSession() as session:
        fetch_awaitables = [
            fetch(session,
                  f'https://api.nasa.gov/neo/rest/v1/feed?start_date='
                  f'{start_date}&end_date={start_date + datetime.timedelta(days=6)}&api_key={API_KEY}')
            for start_date in start_dates
        ]
        return sum(await asyncio.gather(*fetch_awaitables))

currencies = asyncio.run(collect())  # 853 asteroids
# print(currencies)
# print(json.dumps(currencies, indent=4, ensure_ascii=False))

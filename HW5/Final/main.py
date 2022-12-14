import platform
import aiohttp, asyncio
import json, os
from pprint import pprint
from time import time
from datetime import datetime, timedelta

def create_dates() -> list[str]:
    days: int = int(input('Введіть кількість днів(max 10): ')) 
    if days > 10:
        days = days - days % 10
    today: datetime = datetime.today()
    return [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]


def get_currencies():
    currencies = input('Введіть валюти ("usd", "eur" або "usd eur"): ').split()
    return  [currency.upper().strip() for currency in currencies]


def get_currencies_data(data: dict, searched_currencies: list[str] = ('USD', 'EUR')) -> dict:
    currencies_data: list = [d for d in data['exchangeRate'] if d["currency"] in searched_currencies]
    all_currencies_info: dict = {}
    for currency, currency_data in zip(searched_currencies, currencies_data):
        currency_exchange_info: dict = {'sale': round(currency_data['saleRate'], 2), 'purchase': round(currency_data['purchaseRate'], 2)}
        all_currencies_info.update({currency: currency_exchange_info})
    return {data['date']: all_currencies_info}


def write_in_json(data: dict) -> None:
    with open('data.json', 'a') as file:
        json.dump(data, file, indent=2)


async def get_rate_by_date(session, url, currencies):
    before = time()
    print(f'Getting currency rate for {url[-10:]}...')
    async with session.get(url) as response:
        print(f"Status for {url[-10:]}:", response.status)
        all_currencies = await response.json()
        correct_data = get_currencies_data(all_currencies, currencies)
        write_in_json(correct_data)
        print(f'Searching time for {url[-10:]} took {time() - before} sec\n')
        return correct_data

async def main():
    async with aiohttp.ClientSession() as session:
        urls = [f'https://api.privatbank.ua/p24api/exchange_rates?date={date}' for date in create_dates()]
        currencies = get_currencies()
        tasks = [asyncio.create_task(get_rate_by_date(session, url, currencies)) for url in urls]
        responses = await asyncio.gather(*tasks)
        pprint(responses)




if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    before = time()
    asyncio.run(main())
    print(f'Main func with waiting for user input took {time() - before} sec')
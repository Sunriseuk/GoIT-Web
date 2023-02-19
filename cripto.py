import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Запросить API ключ и секретный ключ на Binance и вставить их ниже
api_key = 'ZiOyqE8TTLqaCP1d5FS4DjeU1V2gxggpUUjJQ6wlkhPqs6PiX9O5fobdgcZFWVv1'
api_secret = '5ddyucDFUR8TtWqdn2FrP3cn4znGTAJNFxisbKg27o8fFmCNunHibhQt1gcfWtfr'

# Функция для получения курса криптовалюты из Binance API
def get_crypto_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        print(f"Error: Could not retrieve price data for {symbol}")
        return None

# Запросить у пользователя ввод названия криптовалюты
crypto_name = input("Введите название криптовалюты (например, BTCUSDT): ")

# Получить цену криптовалюты на данный момент
price = get_crypto_price(crypto_name)

if price is not None:
    # Задать диапазон времени (от текущей даты минус 1 месяц)
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() * 1000)

    # Сделать запрос к Binance API для получения исторических данных цены
    url = f"https://api.binance.com/api/v3/klines?symbol={crypto_name}&interval=1d&startTime={start_time}&endTime={end_time}"
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Преобразовать полученные данные в DataFrame
        data = response.json()
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Нарисовать график цены за последний месяц
        plt.figure(figsize=(12, 6))
        plt.plot(df["close"])
        plt.title(f"{crypto_name} Price History")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()
    else:
        print(f"Error: Could not retrieve historical price data for {crypto_name}")
else:
    print(f"Error: Could not retrieve current price data for {crypto_name}")

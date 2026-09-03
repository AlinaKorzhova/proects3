import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
HEADERS = {"apikey": API_KEY}

def function(transaction: dict) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму
    транзакции в рублях. Если транзакция была в USD или EUR,
    происходит обращение к внешнему API для получения текущего
    курса валют и конвертации суммы операции в рубли"""
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]
    if currency == "RUB":
        return amount
    if not API_KEY:
        print("Ошибка: Не установлен API-ключ для Exchange Rates Data API")
        return 0.0
    to_currency = "RUB"
    response = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={currency}&amount={amount}", headers=HEADERS, data={}
        )
    return response.json().get("result", "Сервер не выдал ответа")


if __name__ == "__main__":
    transaction = {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }
    print(function(transaction))

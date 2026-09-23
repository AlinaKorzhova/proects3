import re
from collections import Counter


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Оплата",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Вклады",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Покупки",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


categories = ["Покупки", "Перевод со счета на счет", "Перевод с карты на карту", "Вклады", "Оплата"]


def process_bank_search(transactions: list[dict], search_pattern: str) -> list[dict]:
    """Функция, принимает список словарей с данными о банковских операциях
    и строку поиска, а возвращает список словарей, у которых в описании
    есть данная строка."""
    pattern = re.compile(search_pattern)
    list_search = []
    for transaction in transactions:
        description = transaction.get("description", "")

        if pattern.search(description):
            list_search.append(transaction)

    return list_search


print(process_bank_search(transactions, r"Перевод"))


def process_bank_operations(transactions: list[dict], categories: list) -> dict:
    """Функция,принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращать словарь, в котором ключи — это названия категорий, а значения — это количество операций
    в каждой категории. Категории операций хранятся в поле description."""
    list_operations = []

    for transaction in transactions:
        description = transaction.get("description", "")
        desc_lower = description.lower()
        for category in categories:
            if category.lower() in desc_lower:
                list_operations.append(category)
    count = Counter(list_operations)
    return count


print(process_bank_operations(transactions, categories))

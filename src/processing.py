from typing import Any


def filter_by_state(transactions: list, state: str = "EXECUTED") -> list[Any] | str:
    """Функция фильтрует по "state" """
    try:
        result = []
        for transaction in transactions:
            if transaction["state"] == state:
                result.append(transaction)
        return result
    except ValueError:
        return "Неверный формат данных"


def sort_by_date(transactions: list, reverse: bool =True) -> list[Any] | str:
    """Функция сортирует по дате
    :rtype: list[Any] | str
    """
    try:
        sort_func = sorted(transactions, key=lambda x: x["date"], reverse=reverse)
        return sort_func
    except ValueError:
        return "Неверный формат данных"


if __name__ == "__main__":
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(transactions))
    print(sort_by_date(transactions))

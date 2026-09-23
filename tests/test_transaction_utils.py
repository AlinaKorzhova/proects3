import unittest
from unittest.mock import patch

from src.transaction_utils import process_bank_operations, process_bank_search

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


def test_process_bank_search():
    result = process_bank_search(transactions, r"перевод")
    assert len(result) == 0


def test_no_matches():
    result = process_bank_search(transactions, r"перевод")
    assert (result, [])


@patch("re.compile")
def test_uses_re_compile(mock_compile):
    # Проверяем, что функция реально использует re.compile
    mock_compile.return_value.search.return_value = True
    transactions = [{"id": 1, "description": "любой текст"}]
    process_bank_search(transactions, r"шаблон")
    mock_compile.assert_called_once()


def test_process_bank_operations():
    result = process_bank_operations(transactions, categories)
    assert result["Перевод со счета на счет"] == 1
    assert result["Оплата"] == 1
    assert result["Вклады"] == 1
    assert result["Покупки"] == 1
    assert result["Перевод с карты на карту"] == 1


if __name__ == "__main__":
    unittest.main()

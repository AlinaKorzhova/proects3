import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.utils import read_json_file
from src.pandas_csv import open_csv_reader, open_excel_reader
from src.processing import filter_by_state, sort_by_date
from src.transaction_utils import process_bank_search
from src.widget import mask_account_card
from src.external_api import function


def format_amount(transaction: Dict[str, Any]) -> str:
    """Форматирует сумму с валютой: 40542 руб."""
    amount = transaction.get("amount", "")
    currency = transaction.get("currency_code", "")
    currency_map = {"RUB": "руб.", "USD": "USD", "EUR": "EUR"}
    currency_name = currency_map.get(currency, currency)
    return f"{amount} {currency_name}"


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода."""
    # Дата: 2023-09-05T11:30:32Z -> 05.09.2023
    date_str = transaction.get("date", "")
    try:
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        dt = datetime.fromisoformat(date_str)
        date_formatted = dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        date_formatted = date_str

    description = transaction.get("description", "")

    # Откуда и куда
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    if from_account and to_account:
        accounts_line = f"{mask_account_card(from_account)} -> {mask_account_card(to_account)}"
    elif to_account:
        accounts_line = mask_account_card(to_account)
    elif from_account:
        accounts_line = mask_account_card(from_account)
    else:
        accounts_line = ""

    amount_line = f"Сумма: {format_amount(transaction)}"

    lines = [date_formatted, description]
    if accounts_line:
        lines.append(accounts_line)
    lines.append(amount_line)

    return "\n".join(lines)


# ─── Вспомогательные функции ввода ───────────────────────────

def ask_yes_no(prompt: str) -> bool:
    """Спрашивает Да/Нет, возвращает True/False."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print('Введите "Да" или "Нет"')

VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]

def ask_status() -> str:
    """Запрашивает статус у пользователя с проверкой корректности."""
    while True:
        print(
            'Введите статус, по которому необходимо выполнить фильтрацию.\n'
            'Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING'
        )
        status = input().strip().upper()
        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Статус операции "{status}" недоступен.\n')


# ─── Главная функция ─────────────────────────────────────────

def main() -> None:
    """Основная логика: меню, фильтрация, сортировка, вывод."""

    # 1. Приветствие и выбор источника данных
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    # Запрашиваем путь к файлу и читаем данные
    transactions: List[Dict[str, Any]] = []

    while True:
        choice = input().strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            filepath = input("Введите путь к файлу: ").strip()
            transactions = read_json_file(filepath)
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            filepath = input("Введите путь к файлу: ").strip()
            transactions = open_csv_reader(filepath)
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            filepath = input("Введите путь к файлу: ").strip()
            transactions = open_excel_reader(filepath)
            break
        else:
            print("Неверный пункт меню. Введите 1, 2 или 3.")

    # 2. Фильтрация по статусу
    status = ask_status()
    transactions = filter_by_state(transactions, status)

    # 3. Сортировка по дате
    if ask_yes_no("Отсортировать операции по дате? Да/Нет\n"):
        while True:
            order = input(
                "Отсортировать по возрастанию или по убыванию?\n"
            ).strip().lower()
            if "возраст" in order:
                transactions = sort_by_date(transactions, reverse=False)
                break
            if "убыван" in order:
                transactions = sort_by_date(transactions, reverse=True)
                break
            print('Введите "по возрастанию" или "по убыванию"')

    # 4. Только рублёвые
    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет\n"):
        transactions = function(transactions)

    # 5. Фильтр по слову в описании
    if ask_yes_no(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
    ):
        word = input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, word)

    # 6. Вывод результата
    print("Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    for tx in transactions:
        print(format_transaction(tx))
        print()


if __name__ == "__main__":
    main()

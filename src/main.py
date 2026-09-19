import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


# ─── Чтение данных ───────────────────────────────────────────

def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """Читает транзакции из JSON-файла."""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def load_transactions_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """Читает транзакции из CSV-файла (через pandas)."""
    import pandas as pd
    df = pd.read_csv(filepath)
    return df.to_dict(orient="records")


def load_transactions_from_xlsx(filepath: str) -> List[Dict[str, Any]]:
    """Читает транзакции из XLSX-файла (через pandas)."""
    import pandas as pd
    df = pd.read_excel(filepath)
    return df.to_dict(orient="records")


# ─── Фильтрация ──────────────────────────────────────────────

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрует по статусу (регистронезависимо)."""
    status_upper = status.strip().upper()
    return [tx for tx in transactions if tx.get("state", "").upper() == status_upper]


def filter_by_ruble(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только рублёвые транзакции."""
    return [tx for tx in transactions if tx.get("currency_code", "") == "RUB"]


def filter_by_word(
    transactions: List[Dict[str, Any]], word: str
) -> List[Dict[str, Any]]:
    """Фильтрует по слову в описании (регистронезависимо)."""
    word_lower = word.lower()
    return [
        tx
        for tx in transactions
        if isinstance(tx.get("description", ""), str)
        and word_lower in tx["description"].lower()
    ]


# ─── Сортировка ──────────────────────────────────────────────

def sort_by_date(
    transactions: List[Dict[str, Any]], reverse: bool = False
) -> List[Dict[str, Any]]:
    """Сортирует по дате. reverse=True — по убыванию."""

    def parse_date(tx: Dict[str, Any]) -> datetime:
        date_str = tx.get("date", "")
        if isinstance(date_str, datetime):
            return date_str
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        return datetime.fromisoformat(date_str)

    return sorted(transactions, key=parse_date, reverse=reverse)


# ─── Форматирование вывода ──────────────────────────────────

def mask_account(account: str) -> str:
    """
    Маскирует номер счёта или карты.
    Для счёта: Счет **1234
    Для карты: Visa Platinum 1234 56** **** 7890
    """
    if not account:
        return ""

    # Если начинается с "Счет" — маскируем как счёт
    if account.lower().startswith("счет"):
        number = account.replace("Счет", "").replace("счет", "").strip()
        return f"Счет **{number[-4:]}" if len(number) >= 4 else f"Счет **{number}"

    # Иначе — это карта: "Visa Platinum 7492 6511 6651 7202"
    parts = account.split()
    if len(parts) < 2:
        return account

    # Тип карты — это всё, кроме последней части (номера)
    card_type = " ".join(parts[:-1])
    number = parts[-1]

    if len(number) >= 16:
        # Формат: 1234 56** **** 7890
        masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    elif len(number) >= 4:
        masked = f"{number[:4]} **{number[-2:]}"
    else:
        masked = number

    return f"{card_type} {masked}"


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
        accounts_line = f"{mask_account(from_account)} -> {mask_account(to_account)}"
    elif to_account:
        accounts_line = mask_account(to_account)
    elif from_account:
        accounts_line = mask_account(from_account)
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
            transactions = load_transactions_from_json(filepath)
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            filepath = input("Введите путь к файлу: ").strip()
            transactions = load_transactions_from_csv(filepath)
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            filepath = input("Введите путь к файлу: ").strip()
            transactions = load_transactions_from_xlsx(filepath)
            break
        else:
            print("Неверный пункт меню. Введите 1, 2 или 3.")

    # 2. Фильтрация по статусу
    status = ask_status()
    transactions = filter_by_status(transactions, status)

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
        transactions = filter_by_ruble(transactions)

    # 5. Фильтр по слову в описании
    if ask_yes_no(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
    ):
        word = input("Введите слово для поиска: ").strip()
        transactions = filter_by_word(transactions, word)

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

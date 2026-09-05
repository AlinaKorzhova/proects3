from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_account_number: str) -> str:
    """Маскирует номер и счет"""
    try:
        split_card_account = card_account_number.split()
        card_name = " ".join(split_card_account[:-1])
        card_number = split_card_account[-1]
        if "счет" in card_name.lower():
            hidden_num = get_mask_account(card_number)
        else:
            hidden_num = get_mask_card_number(card_number)
        result_ = f"{card_name} {hidden_num}"
        return result_
    except ValueError:
        return "Неверный формат данных"


def get_date(date_string: str) -> str:
    """преобразует дату в нужный формат"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return "Неверный формат данных"


if __name__ == "__main__":
    print(mask_account_card("Visa Card 7000792289606367"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))

    print(get_date("2024-03-11T02:26:18.671407"))

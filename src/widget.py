from masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(card_account_number: str) -> str:
    """Маскирует номер и счет """
    card_name, card_number = card_account_number.split(" ", 1)
    try:
        if "счет" in card_name.lower():
            hidden_num = get_mask_account(card_number)
        else:
            hidden_num = get_mask_card_number(card_number)
        result_ = f"{card_name} {hidden_num}"
        return result_
    except ValueError:
        return "Неверный формат данных"


#print(mask_account_card("MasterCard   7000792289606367"))
print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))

def get_date(date_string: str) -> str:
    """преобразует дату в нужный формат"""
    dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
    return dt.strftime("%d.%m.%Y")


print(get_date("2024-03-11T02:26:18.671407"))


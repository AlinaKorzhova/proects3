def get_mask_card_number(number: str) -> str:
    if len(number) == 16:
        return number[:4] + " " + number[4:6] + "** **** " + number[-4:]
    return "Неверный формат данных"


def get_mask_account(account_number: str) -> str:
    if len(account_number) >= 4:
        return "**" + account_number[-4:]
    return "Неверный формат данных"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("7000792289606361"))

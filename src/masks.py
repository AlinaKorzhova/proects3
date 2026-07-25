def get_mask_card_number(number: str) -> str:
    number = str(number)
    if len(number) == 16:
      result = number[:4] + " " + number[4:6] + "** **** " + number[-4:]
    return result


print(get_mask_card_number("7000792289606361"))


def get_mask_account(account_number: str) -> str:
    account_number = str(account_number)
    if len(account_number) >= 4:
      total = "**" + account_number[-4:]
    return total


print(get_mask_account("7000792289606361"))

import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/masks.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number: str) -> str:
    """Маскирует номер карты 1111 11** **** 1111"""
    logger.info("Длину карты {len(number) == 16} равна 16 символов")
    if len(number) == 16:
        return number[:4] + " " + number[4:6] + "** **** " + number[-4:]
    logger.error("Неверный формат данных")
    return "Неверный формат данных"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета **1111"""
    logger.info("Длина счета {len(account_number) >= 4} больше 4 символов")
    if len(account_number) >= 4:
        return "**" + account_number[-4:]
    logger.error("Неверный формат данных")
    return "Неверный формат данных"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("7000792289606361"))

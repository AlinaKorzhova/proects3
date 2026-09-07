import json
import logging
from typing import Dict, List

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def read_json_file(file_path: str = "../data/operations.json") -> List[Dict]:
    """
     Загружает данные о финансовых транзакциях из JSON-файла.
    Если файл пустой, содержит не список или не найден,
    функция возвращает пустой список.
    """
    try:
        logger.info(f"Читается operations.json ")
        logger.debug(f"Открытие файла по пути: {file_path}")
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError, OSError) as ex:
        logging.error(f"Произошла ошибка: {ex}")
        return []

if __name__ == "__main__":
    print(read_json_file("../data/operations.json"))



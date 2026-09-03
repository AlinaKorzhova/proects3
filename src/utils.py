import json
from typing import Dict, List


def read_json_file(file_path: str = "../data/operations.json") -> List[Dict]:
    """
     Загружает данные о финансовых транзакциях из JSON-файла.
    Если файл пустой, содержит не список или не найден,
    функция возвращает пустой список.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

if __name__ == "__main__":
    print(read_json_file("../data/operations.json"))



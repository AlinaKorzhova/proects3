from pathlib import Path

import pandas as pd

def open_csv_reader(path_to_file: Path) -> list[dict]:
    df = pd.read_csv(path_to_file)
    data_dict_csv = df.to_dict(orient="records")
    return data_dict_csv


def open_excel_reader(path_to_file: Path) -> list[dict]:
    df = pd.read_excel(path_to_file)
    data_dict_excel = df.to_dict(orient="records")
    return data_dict_excel

if __name__ == "__main__":

    # print("Вывод данных из .csv файла")
    # transactions = open_csv_reader(Path("../data/transactions.csv"))
    # for row in transactions:
    #     print(row)

    print("Вывод данных из .xlsx файла")
    transactions = open_excel_reader(Path("../data/transactions_excel.xlsx"))
    for row in transactions:
        print(row)
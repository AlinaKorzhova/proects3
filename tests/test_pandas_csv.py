from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.pandas_csv import open_csv_reader, open_excel_reader

fake_data = {
    "id": [1, 2],
    "state": ["EXECUTED", "CANCELED"],
    "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
    "amount": [16210, 29740],
    "currency_name": ["Sol", "Peso"],
    "currency_code": ["PEN", "COP"],
    "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
    "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
    "description": ["Перевод организации", "Перевод с карты на карту"],
}

expected_output = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": 16210,
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации",
    },
    {
        "id": 2,
        "state": "CANCELED",
        "date": "2020-12-06T23:00:58Z",
        "amount": 29740,
        "currency_name": "Peso",
        "currency_code": "COP",
        "from": "Discover 3172601889670065",
        "to": "Discover 0720428384694643",
        "description": "Перевод с карты на карту",
    },
]


@patch("src.pandas_csv.pd.read_csv")  # важно: патч по месту использования в src.pandas_csv
def test_open_csv_reader(mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame(fake_data)
    result = open_csv_reader(Path("dummy_path.csv"))
    assert result == expected_output


@patch("src.pandas_csv.pd.read_excel")  # важно: патч по месту использования в src.pandas_csv
def test_open_excel_reader(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame(fake_data)
    result = open_excel_reader(Path("dummy_path_2.xlsx"))
    assert result == expected_output

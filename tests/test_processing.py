import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture()
def transactions():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state(transactions):
    assert filter_by_state(transactions, "EXECUTED") == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    assert filter_by_state(transactions, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    assert filter_by_state(transactions, "NOMUR") == []


@pytest.mark.parametrize(
    "state, expected_output",
    [
        ("active", []),
        ("inactive", [{"state": "inactive"}]),
        ("unknown", []),
    ],
)
def test_filter_by_state_(state, expected_output):
    data = [{"state": "inactive"}]
    assert filter_by_state(data, state) == expected_output


def test_sort_by_date(transactions, reverse=True):
    assert sort_by_date(transactions) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    assert sort_by_date(transactions, False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date_with_same_dates():
    dt = [
        {"date": "2023-10-01", "id": 2},
        {"date": "2023-10-01", "id": 1},
    ]
    expected_output = [
        {"date": "2023-10-01", "id": 2},
        {"date": "2023-10-01", "id": 1},
    ]
    assert sort_by_date(dt) == expected_output


def test_sort_by_date_with_incorrect_formats():
    dt = [
        {"date": "2023/10/01", "id": 1},
        {"date": "10-01-2023", "id": 2},
        {"date": "not-a-date", "id": 3},
    ]

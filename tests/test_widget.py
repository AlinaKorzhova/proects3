import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "split_card_account, result_",
    [
        ("Visa Card 7000792289606367", "Visa Card 7000 79** **** 6367"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
    ],
)
def test_mask_account_card(split_card_account, result_):
    assert mask_account_card(split_card_account) == result_


def test_mask_account_card_name():
    assert mask_account_card("xx99")

    assert mask_account_card("fffffffffff")

    assert mask_account_card("Visa 99999999999999999")

    assert mask_account_card("Счёт 8976")


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407")

    assert get_date("10112011")

    assert get_date("None")

    assert get_date("2023 / 10 / 15abc")

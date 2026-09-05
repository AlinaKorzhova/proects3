import pytest
from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize("split_card_account, result_", [("Visa Card 7000792289606367", "Visa Card 7000 79** **** 6367"),
                                                             ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
                                                    ("Счет 64686473678894779589", "Счет **9589"),
                                                         ("xx99", " Неверный формат данных"),
                                                         ("yyyyyyyyy", " Неверный формат данных")])
def test_mask_account_card(split_card_account, result_):
    assert mask_account_card(split_card_account) == result_



def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407")

    assert get_date("2024")

    assert get_date("")

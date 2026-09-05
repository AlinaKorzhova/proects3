from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number():
    assert get_mask_card_number("7567463548210976")

    assert get_mask_card_number("666666")

    assert get_mask_card_number("None")

    assert get_mask_card_number("dfssdfghhjjjgffdsddd")


def test_get_mask_account():
    assert get_mask_account("67543488767")

    assert get_mask_account("88")

    assert get_mask_account("None")

    assert get_mask_account("fdhbdedaefegrsgs")

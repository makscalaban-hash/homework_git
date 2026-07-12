import pytest

from src.masks.masking import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    def test_masks_valid_card_number(self, valid_card_number: str) -> None:
        assert get_mask_card_number(valid_card_number) == "7000 79** **** 6361"

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1111222233334444", "1111 22** **** 4444"),
            ("0000000000000000", "0000 00** **** 0000"),
        ],
    )
    def test_masks_various_card_numbers(self, card_number: str, expected: str) -> None:
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "invalid_card_number",
        [
            "700079228960636",  # 15 цифр — короче нужного
            "70007922896063611",  # 17 цифр — длиннее нужного
            "700079228960636a",  # содержит не только цифры
            "",  # номер отсутствует
        ],
    )
    def test_raises_on_invalid_card_number(self, invalid_card_number: str) -> None:
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_card_number)


class TestGetMaskAccount:
    def test_masks_valid_account_number(self, valid_account_number: str) -> None:
        assert get_mask_account(valid_account_number) == "**4305"

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654108430135874305", "**4305"),
            ("1234", "**1234"),
            ("00004321", "**4321"),
        ],
    )
    def test_masks_various_account_numbers(
        self, account_number: str, expected: str
    ) -> None:
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize(
        "invalid_account_number",
        [
            "123",  # меньше 4 цифр
            "12a4",  # содержит не только цифры
            "",  # номер отсутствует
        ],
    )
    def test_raises_on_invalid_account_number(
        self, invalid_account_number: str
    ) -> None:
        with pytest.raises(ValueError):
            get_mask_account(invalid_account_number)

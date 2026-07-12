import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    @pytest.mark.parametrize(
        "info, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ],
    )
    def test_masks_card_or_account_depending_on_input(
        self, info: str, expected: str
    ) -> None:
        assert mask_account_card(info) == expected

    @pytest.mark.parametrize(
        "invalid_info",
        [
            "",  # пустая строка
            "   ",  # строка из одних пробелов
            "OnlyOneWord",  # нет номера
            "Visa Platinum 700079228960636a",  # некорректный номер
        ],
    )
    def test_raises_on_invalid_input(self, invalid_info: str) -> None:
        with pytest.raises(ValueError):
            mask_account_card(invalid_info)


class TestGetDate:
    @pytest.mark.parametrize(
        "date_str, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2019-07-03T18:35:29.512364", "03.07.2019"),
            ("2000-01-01T00:00:00.000000", "01.01.2000"),
        ],
    )
    def test_converts_valid_dates(self, date_str: str, expected: str) -> None:
        assert get_date(date_str) == expected

    @pytest.mark.parametrize(
        "invalid_date_str",
        [
            "",  # дата отсутствует
            "not-a-date",  # произвольная строка
            "11.03.2024",  # не ISO-формат
        ],
    )
    def test_raises_on_invalid_date(self, invalid_date_str: str) -> None:
        with pytest.raises(ValueError):
            get_date(invalid_date_str)

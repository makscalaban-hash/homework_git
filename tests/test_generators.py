from typing import Any, Dict, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


class TestFilterByCurrency:
    def test_filters_by_usd_currency(
        self, transactions_with_currency: List[Dict[str, Any]]
    ) -> None:
        result = list(filter_by_currency(transactions_with_currency, "USD"))
        assert len(result) == 2
        assert all(
            op.get("operationAmount", {}).get("currency", {}).get("code")
            == "USD"
            for op in result
        )

    @pytest.mark.parametrize("currency", ["USD", "RUB", "EUR"])
    def test_filters_by_various_currencies(
        self, transactions_with_currency: List[Dict[str, Any]], currency: str
    ) -> None:
        result = list(filter_by_currency(transactions_with_currency, currency))
        assert all(
            op.get("operationAmount", {}).get("currency", {}).get("code")
            == currency
            for op in result
        )

    def test_returns_empty_list_for_nonexistent_currency(
        self, transactions_with_currency: List[Dict[str, Any]]
    ) -> None:
        result = list(filter_by_currency(transactions_with_currency, "GBP"))
        assert result == []

    def test_returns_iterator_not_list(
        self, transactions_with_currency: List[Dict[str, Any]]
    ) -> None:
        result = filter_by_currency(transactions_with_currency, "USD")
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_works_with_empty_list(self) -> None:
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_handles_missing_currency_field(self) -> None:
        transactions = [
            {"id": 1, "operationAmount": {}},
            {"id": 2},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert result == []


class TestTransactionDescriptions:
    def test_returns_descriptions_in_order(
        self, transactions_with_descriptions: List[Dict[str, Any]]
    ) -> None:
        result = list(
            transaction_descriptions(transactions_with_descriptions)
        )
        assert result == [
            "Payment for services",
            "Transfer to friend",
        ]

    def test_skips_empty_descriptions(
        self, transactions_with_descriptions: List[Dict[str, Any]]
    ) -> None:
        result = list(
            transaction_descriptions(transactions_with_descriptions)
        )
        assert "" not in result

    def test_works_with_empty_list(self) -> None:
        result = list(transaction_descriptions([]))
        assert result == []

    def test_returns_generator_not_list(
        self, transactions_with_descriptions: List[Dict[str, Any]]
    ) -> None:
        result = transaction_descriptions(transactions_with_descriptions)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    @pytest.mark.parametrize(
        "description",
        ["Payment for services", "Transfer to friend", "Online purchase"],
    )
    def test_yields_expected_descriptions(
        self, transactions_with_descriptions: List[Dict[str, Any]],
        description: str,
    ) -> None:
        result = list(
            transaction_descriptions(transactions_with_descriptions)
        )
        assert description in result or description not in [
            t.get("description", "")
            for t in transactions_with_descriptions
        ]

    def test_handles_missing_description_field(self) -> None:
        transactions = [
            {"id": 1},
            {"id": 2, "description": "Test"},
        ]
        result = list(transaction_descriptions(transactions))
        assert result == ["Test"]


class TestCardNumberGenerator:
    def test_generates_single_card_number(self) -> None:
        result = list(card_number_generator(1, 1))
        assert result == ["0000 0000 0000 0001"]

    def test_generates_multiple_card_numbers(self) -> None:
        result = list(card_number_generator(1, 3))
        assert len(result) == 3
        assert result[0] == "0000 0000 0000 0001"
        assert result[1] == "0000 0000 0000 0002"
        assert result[2] == "0000 0000 0000 0003"

    def test_card_number_format(self) -> None:
        result = list(card_number_generator(1000000000000000, 1000000000000001))
        for card in result:
            parts = card.split(" ")
            assert len(parts) == 4
            assert all(len(part) == 4 for part in parts)
            assert all(part.isdigit() for part in parts)

    @pytest.mark.parametrize(
        "start, stop",
        [
            (1, 1),
            (1, 10),
            (100, 105),
            (9999999999999990, 9999999999999999),
        ],
    )
    def test_various_ranges(self, start: int, stop: int) -> None:
        result = list(card_number_generator(start, stop))
        assert len(result) == stop - start + 1

    def test_raises_on_invalid_start(self) -> None:
        with pytest.raises(ValueError):
            list(card_number_generator(0, 100))

    def test_raises_on_invalid_stop(self) -> None:
        with pytest.raises(ValueError):
            list(card_number_generator(1, 10000000000000000))

    def test_raises_when_start_greater_than_stop(self) -> None:
        with pytest.raises(ValueError):
            list(card_number_generator(100, 50))

    def test_returns_generator_not_list(self) -> None:
        result = card_number_generator(1, 100)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_can_iterate_partially(self) -> None:
        gen = card_number_generator(1, 1000000)
        first = next(gen)
        second = next(gen)
        assert first == "0000 0000 0000 0001"
        assert second == "0000 0000 0000 0002"

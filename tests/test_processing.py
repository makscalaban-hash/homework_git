from typing import Any, Dict, List

import pytest

from src.processing import (
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)


class TestFilterByState:
    def test_default_state_is_executed(
        self, operations_data: List[Dict[str, Any]]
    ) -> None:
        result = filter_by_state(operations_data)
        assert result == [op for op in operations_data if op["state"] == "EXECUTED"]

    @pytest.mark.parametrize("state", ["EXECUTED", "CANCELED", "PENDING"])
    def test_filters_by_various_states(
        self, operations_data: List[Dict[str, Any]], state: str
    ) -> None:
        result = filter_by_state(operations_data, state)
        assert all(op["state"] == state for op in result)
        expected_count = len([op for op in operations_data if op["state"] == state])
        assert len(result) == expected_count

    def test_returns_empty_list_if_state_not_found(
        self, operations_data: List[Dict[str, Any]]
    ) -> None:
        assert filter_by_state(operations_data, "UNKNOWN_STATE") == []

    def test_returns_empty_list_for_empty_input(
        self, operations_empty: List[Dict[str, Any]]
    ) -> None:
        assert filter_by_state(operations_empty) == []

    def test_returns_new_list_not_same_object(
        self, operations_data: List[Dict[str, Any]]
    ) -> None:
        result = filter_by_state(operations_data)
        assert result is not operations_data


class TestSortByDate:
    def test_sorts_descending_by_default(
        self, operations_data: List[Dict[str, Any]]
    ) -> None:
        result = sort_by_date(operations_data)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates, reverse=True)

    def test_sorts_ascending_when_reverse_false(
        self, operations_data: List[Dict[str, Any]]
    ) -> None:
        result = sort_by_date(operations_data, reverse=False)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates)

    def test_duplicate_dates_keep_original_relative_order(
        self, operations_with_duplicate_dates: List[Dict[str, Any]]
    ) -> None:
        result = sort_by_date(operations_with_duplicate_dates)
        assert [op["id"] for op in result] == [1, 2]

    def test_returns_empty_list_for_empty_input(
        self, operations_empty: List[Dict[str, Any]]
    ) -> None:
        assert sort_by_date(operations_empty) == []

    def test_returns_new_list_not_same_object(
        self, operations_data: List[Dict[str, Any]]
    ) -> None:
        result = sort_by_date(operations_data)
        assert result is not operations_data

    def test_handles_non_standard_date_strings_without_error(self) -> None:
        operations = [
            {"id": 1, "date": "not-a-real-date"},
            {"id": 2, "date": "2020-01-01"},
        ]
        result = sort_by_date(operations)
        assert len(result) == 2


class TestProcessBankSearch:
    @pytest.fixture
    def operations_for_search(self) -> List[Dict[str, Any]]:
        return [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Открытие вклада"},
            {"id": 4, "description": "Оплата (интернет)"},
        ]

    def test_finds_operations_by_search_string(
        self, operations_for_search: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_search(operations_for_search, "перевод")
        assert [op["id"] for op in result] == [1, 2]

    def test_search_is_case_insensitive(
        self, operations_for_search: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_search(operations_for_search, "ПЕРЕВОД")
        assert [op["id"] for op in result] == [1, 2]

    def test_returns_empty_list_when_no_match(
        self, operations_for_search: List[Dict[str, Any]]
    ) -> None:
        assert process_bank_search(operations_for_search, "ипотека") == []

    def test_returns_all_data_when_search_is_empty_string(
        self, operations_for_search: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_search(operations_for_search, "")
        assert result == operations_for_search

    def test_returns_empty_list_for_empty_input(
        self, operations_empty: List[Dict[str, Any]]
    ) -> None:
        assert process_bank_search(operations_empty, "перевод") == []

    def test_special_characters_in_search_are_treated_literally(
        self, operations_for_search: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_search(operations_for_search, "(интернет)")
        assert [op["id"] for op in result] == [4]


class TestProcessBankOperations:
    @pytest.fixture
    def operations_for_categories(self) -> List[Dict[str, Any]]:
        return [
            {"id": 1, "description": "Открытие вклада"},
            {"id": 2, "description": "Открытие вклада"},
            {"id": 3, "description": "Перевод организации"},
            {"id": 4, "description": "Без категории"},
        ]

    def test_counts_operations_per_category(
        self, operations_for_categories: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_operations(
            operations_for_categories, ["Открытие вклада", "Перевод организации"]
        )
        assert result == {"Открытие вклада": 2, "Перевод организации": 1}

    def test_returns_zero_for_category_with_no_matches(
        self, operations_for_categories: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_operations(operations_for_categories, ["Ипотека"])
        assert result == {"Ипотека": 0}

    def test_returns_empty_dict_for_empty_categories(
        self, operations_for_categories: List[Dict[str, Any]]
    ) -> None:
        assert process_bank_operations(operations_for_categories, []) == {}

    def test_returns_zero_counts_for_empty_input(
        self, operations_empty: List[Dict[str, Any]]
    ) -> None:
        result = process_bank_operations(operations_empty, ["Открытие вклада"])
        assert result == {"Открытие вклада": 0}

    def test_operations_without_description_are_ignored(self) -> None:
        operations: List[Dict[str, Any]] = [
            {"id": 1, "description": "Открытие вклада"},
            {"id": 2},
        ]
        result = process_bank_operations(operations, ["Открытие вклада"])
        assert result == {"Открытие вклада": 1}

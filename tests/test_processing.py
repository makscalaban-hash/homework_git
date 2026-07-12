from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


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

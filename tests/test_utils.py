from unittest.mock import mock_open, patch

from src.utils import read_operations_from_json


class TestReadOperationsFromJson:
    def test_reads_valid_json_file(self) -> None:
        json_data = '[{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]'
        with patch("src.utils.os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=json_data)
        ):
            result = read_operations_from_json("data/operations.json")
        expected = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]
        assert result == expected

    def test_returns_empty_list_if_file_not_found(self) -> None:
        with patch("src.utils.os.path.exists", return_value=False):
            result = read_operations_from_json("data/missing.json")
        assert result == []

    def test_returns_empty_list_if_file_is_empty(self) -> None:
        with patch("src.utils.os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data="")
        ):
            result = read_operations_from_json("data/empty.json")
        assert result == []

    def test_returns_empty_list_if_content_is_not_a_list(self) -> None:
        with patch("src.utils.os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data='{"id": 1, "state": "EXECUTED"}')
        ):
            result = read_operations_from_json("data/operations.json")
        assert result == []

    def test_returns_empty_list_on_invalid_json(self) -> None:
        with patch("src.utils.os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data="not valid json{{{")
        ):
            result = read_operations_from_json("data/broken.json")
        assert result == []

from unittest.mock import Mock, patch

from src.readers import read_operations_from_csv, read_operations_from_excel


class TestReadOperationsFromCsv:
    def test_reads_valid_csv_file(self) -> None:
        mock_dataframe = Mock()
        mock_dataframe.to_dict.return_value = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]
        with patch("src.readers.os.path.exists", return_value=True), patch(
            "src.readers.pd.read_csv", return_value=mock_dataframe
        ) as mock_read_csv:
            result = read_operations_from_csv("data/transactions.csv")

        assert result == [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]
        mock_read_csv.assert_called_once_with("data/transactions.csv", sep=";")
        mock_dataframe.to_dict.assert_called_once_with(orient="records")

    def test_returns_empty_list_if_file_not_found(self) -> None:
        with patch("src.readers.os.path.exists", return_value=False):
            result = read_operations_from_csv("data/missing.csv")
        assert result == []

    def test_returns_empty_list_on_empty_data_error(self) -> None:
        import pandas as pd

        with patch("src.readers.os.path.exists", return_value=True), patch(
            "src.readers.pd.read_csv", side_effect=pd.errors.EmptyDataError()
        ):
            result = read_operations_from_csv("data/empty.csv")
        assert result == []

    def test_returns_empty_list_on_parser_error(self) -> None:
        import pandas as pd

        with patch("src.readers.os.path.exists", return_value=True), patch(
            "src.readers.pd.read_csv", side_effect=pd.errors.ParserError()
        ):
            result = read_operations_from_csv("data/broken.csv")
        assert result == []


class TestReadOperationsFromExcel:
    def test_reads_valid_excel_file(self) -> None:
        mock_dataframe = Mock()
        mock_dataframe.to_dict.return_value = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]
        with patch("src.readers.os.path.exists", return_value=True), patch(
            "src.readers.pd.read_excel", return_value=mock_dataframe
        ) as mock_read_excel:
            result = read_operations_from_excel("data/transactions_excel.xlsx")

        assert result == [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]
        mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")
        mock_dataframe.to_dict.assert_called_once_with(orient="records")

    def test_returns_empty_list_if_file_not_found(self) -> None:
        with patch("src.readers.os.path.exists", return_value=False):
            result = read_operations_from_excel("data/missing.xlsx")
        assert result == []

    def test_returns_empty_list_on_value_error(self) -> None:
        with patch("src.readers.os.path.exists", return_value=True), patch(
            "src.readers.pd.read_excel", side_effect=ValueError()
        ):
            result = read_operations_from_excel("data/broken.xlsx")
        assert result == []

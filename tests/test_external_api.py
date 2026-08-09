from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


class TestConvertToRub:
    def test_rub_transaction_returns_amount_without_api_call(
        self, transaction_rub: Dict[str, Any]
    ) -> None:
        with patch("src.external_api.requests.get") as mock_get:
            result = convert_to_rub(transaction_rub)
        assert result == 500.0
        mock_get.assert_not_called()

    @patch("src.external_api.requests.get")
    def test_usd_transaction_calls_api_and_converts(
        self, mock_get: Mock, transaction_usd: Dict[str, Any]
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"result": 9250.75}
        mock_get.return_value = mock_response

        result = convert_to_rub(transaction_usd)

        assert result == 9250.75
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_eur_transaction_calls_api_and_converts(
        self, mock_get: Mock, transaction_eur: Dict[str, Any]
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"result": 10120.40}
        mock_get.return_value = mock_response

        result = convert_to_rub(transaction_eur)

        assert result == 10120.40
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_result_is_float_type(
        self, mock_get: Mock, transaction_usd: Dict[str, Any]
    ) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"result": "9300.0"}
        mock_get.return_value = mock_response

        result = convert_to_rub(transaction_usd)

        assert isinstance(result, float)

    @patch("src.external_api.requests.get")
    def test_raises_on_http_error(
        self, mock_get: Mock, transaction_usd: Dict[str, Any]
    ) -> None:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API error")
        mock_get.return_value = mock_response

        with pytest.raises(Exception):
            convert_to_rub(transaction_usd)

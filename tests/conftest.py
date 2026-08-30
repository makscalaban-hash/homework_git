from typing import Any, Dict, List

import pytest


@pytest.fixture
def valid_card_number() -> str:
    """Корректный 16-значный номер карты для тестов маскирования."""
    return "7000792289606361"


@pytest.fixture
def valid_account_number() -> str:
    """Корректный номер банковского счета для тестов маскирования."""
    return "73654108430135874305"


@pytest.fixture
def operations_data() -> List[Dict[str, Any]]:
    """Список операций с разными статусами и датами для тестов processing."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 5, "state": "PENDING", "date": "2020-01-01T00:00:00.000000"},
    ]


@pytest.fixture
def operations_with_duplicate_dates() -> List[Dict[str, Any]]:
    """Операции с одинаковой датой — для проверки сортировки при равенстве дат."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2020-01-01T00:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2020-01-01T00:00:00.000000"},
    ]


@pytest.fixture
def operations_empty() -> List[Dict[str, Any]]:
    """Пустой список операций."""
    return []


@pytest.fixture
def transaction_rub() -> Dict[str, Any]:
    """Транзакция в рублях — не должна вызывать внешний API."""
    return {"operationAmount": {"amount": "500.00", "currency": {"code": "RUB"}}}


@pytest.fixture
def transaction_usd() -> Dict[str, Any]:
    """Транзакция в долларах — требует обращения к внешнему API."""
    return {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}


@pytest.fixture
def transaction_eur() -> Dict[str, Any]:
    """Транзакция в евро — требует обращения к внешнему API."""
    return {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}

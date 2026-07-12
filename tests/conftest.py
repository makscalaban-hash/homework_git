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
def transactions_with_currency() -> List[Dict[str, Any]]:
    """Список транзакций с разными валютами для тестов generators."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-15T10:30:00.000000",
            "operationAmount": {
                "amount": "1000",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Payment for services",
            "from": "Visa Platinum 7000 79** **** 6361",
            "to": "Счет **4305",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-01-14T15:20:00.000000",
            "operationAmount": {
                "amount": "5000",
                "currency": {"name": "Russian Ruble", "code": "RUB"},
            },
            "description": "Transfer to friend",
            "from": "Maestro 1596 83** **** 5199",
            "to": "Счет **9876",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-13T12:00:00.000000",
            "operationAmount": {
                "amount": "500",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Online purchase",
            "from": "Visa Classic 4111 11** **** 1111",
            "to": "Счет **5555",
        },
        {
            "id": 4,
            "state": "CANCELED",
            "date": "2024-01-12T09:45:00.000000",
            "operationAmount": {
                "amount": "2000",
                "currency": {"name": "Euro", "code": "EUR"},
            },
            "description": "Refund",
            "from": "Visa Gold 3333 33** **** 3333",
            "to": "Счет **7777",
        },
    ]


@pytest.fixture
def transactions_with_descriptions() -> List[Dict[str, Any]]:
    """Список транзакций с разными описаниями."""
    return [
        {
            "id": 1,
            "description": "Payment for services",
            "operationAmount": {"currency": {"code": "USD"}},
        },
        {
            "id": 2,
            "description": "Transfer to friend",
            "operationAmount": {"currency": {"code": "RUB"}},
        },
        {
            "id": 3,
            "description": "",
            "operationAmount": {"currency": {"code": "EUR"}},
        },
        {
            "id": 4,
            "operationAmount": {"currency": {"code": "USD"}},
        },
    ]

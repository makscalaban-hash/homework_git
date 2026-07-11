from typing import Any, Dict, List


def filter_by_state(
    operations: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует список банковских операций по статусу.

    Args:
        operations: Список словарей с операциями.
        state: Статус для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        Список операций с указанным статусом.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список операций по дате.

    Args:
        operations: Список словарей с операциями.
        reverse: Порядок сортировки (True — по убыванию).

    Returns:
        Отсортированный список операций.
    """
    return sorted(
        operations,
        key=lambda x: x.get("date", ""),
        reverse=reverse,
    )

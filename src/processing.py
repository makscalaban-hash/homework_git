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

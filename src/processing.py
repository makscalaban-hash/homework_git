import re
from collections import Counter
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


def process_bank_search(
    data: List[Dict[str, Any]], search: str
) -> List[Dict[str, Any]]:
    """Фильтрует список транзакций по заданной строке в описании.

    Args:
        data: Список словарей с банковскими операциями.
        search: Строка для поиска в описании операции.

    Returns:
        Список операций, у которых в описании встречается search.
    """
    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        item for item in data
        if item.get("description") and pattern.search(str(item["description"]))
    ]


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Считает количество банковских операций по категориям.

    Категория определяется значением поля description, подсчёт
    выполняется с помощью Counter.

    Args:
        data: Список словарей с банковскими операциями.
        categories: Список категорий (значений поля description),
            по которым нужно посчитать количество операций.

    Returns:
        Словарь, где ключ — категория, значение — количество операций.
    """
    descriptions = [
        str(item["description"])
        for item in data
        if item.get("description") in categories
    ]
    counts = Counter(descriptions)
    return {category: counts.get(category, 0) for category in categories}

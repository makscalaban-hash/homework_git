from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """Фильтрует список транзакций по валюте операции.

    Возвращает итератор, который поочередно выдает транзакции, где валюта
    операции соответствует заданной.

    Args:
        transactions: Список словарей с данными о транзакциях.
        currency: Код валюты для фильтрации (например, 'USD', 'RUB').

    Yields:
        Словарь с транзакцией, у которой валюта соответствует заданной.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        transaction_currency = operation_amount.get("currency", {}).get("code")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(
    transactions: List[Dict[str, Any]],
) -> Generator[str, None, None]:
    """Генератор описаний транзакций.

    Принимает список словарей с транзакциями и возвращает описание каждой
    операции по очереди.

    Args:
        transactions: Список словарей с данными о транзакциях.

    Yields:
        Строка с описанием транзакции.
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор номеров банковских карт в заданном диапазоне.

    Выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X —
    цифра номера карты. Генерирует номера в диапазоне от start до stop
    (включительно).

    Args:
        start: Начальное значение диапазона (от 1 до 9999999999999999).
        stop: Конечное значение диапазона (от 1 до 9999999999999999).

    Yields:
        Строка с номером карты в формате XXXX XXXX XXXX XXXX.

    Raises:
        ValueError: Если start или stop вне диапазона [1, 9999999999999999]
            или start > stop.
    """
    if not (1 <= start <= 9999999999999999):
        raise ValueError(
            "start должен быть в диапазоне [1, 9999999999999999]"
        )
    if not (1 <= stop <= 9999999999999999):
        raise ValueError(
            "stop должен быть в диапазоне [1, 9999999999999999]"
        )
    if start > stop:
        raise ValueError("start не должен быть больше stop")

    for card_num in range(start, stop + 1):
        # Форматируем число как 16-значный номер карты с нулями в начале
        formatted = str(card_num).zfill(16)
        # Разбиваем на группы по 4 цифры
        card_format = (
            f"{formatted[0:4]} {formatted[4:8]} "
            f"{formatted[8:12]} {formatted[12:16]}"
        )
        yield card_format

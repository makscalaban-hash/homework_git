from datetime import datetime
# Импортируем БЕЗ src. на конце, чтобы mypy не сходил с ума
from masks.masking import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в строке.

    Args:
        info (str): Строка формата "Visa Platinum 7000792289606361"
            или "Счет 73654108430135874305"
        info (str): Строка вида "Visa Platinum 7000792289606361"
            или "Счет 73654108430135874305"

    Returns:
        str: Строка с замаскированным номером.
    """
    if not info or len(info.strip()) == 0:
        raise ValueError("Входная строка не должна быть пустой.")

    parts = info.strip().split()
    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер.")

    number = parts[-1]
    description = " ".join(parts[:-1])

    if len(number) == 16 and number.isdigit():
        masked_number = get_mask_card_number(number)
        return f"{description} {masked_number}"
    elif number.isdigit():
        masked_number = get_mask_account(number)
        return f"{description} {masked_number}"
    else:
        raise ValueError("Некорректный формат номера.")


def get_date(date_str: str) -> str:
    """Преобразует дату из ISO-формата в ДД.ММ.ГГГГ."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты.")

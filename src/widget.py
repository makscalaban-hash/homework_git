from datetime import datetime
from src.masks.masking import get_mask_card_number, get_mask_account


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в строке.

    Args:
        info (str): Строка вида "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"

    Returns:
        str: Строка с замаскированным номером.
    """
    if not info or len(info.strip()) == 0:
        raise ValueError("Входная строка не должна быть пустой.")

    parts = info.strip().split()
    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер.")

    # Последние 4 символа — это номер, всё до этого — описание
    number = parts[-1]
    description = " ".join(parts[:-1])

    if len(number) == 16 and number.isdigit():
        # Это карта
        masked_number = get_mask_card_number(number)
        return f"{description} {masked_number}"
    elif number.isdigit():
        # Это счет
        masked_number = get_mask_account(number)
        return f"{description} {masked_number}"
    else:
        raise ValueError("Некорректный формат номера.")


def get_date(date_str: str) -> str:
    """Преобразует дату из ISO-формата в ДД.ММ.ГГГГ.

    Args:
        date_str (str): Дата в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: Дата в формате "11.03.2024"
    """
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты.")

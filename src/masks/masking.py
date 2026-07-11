def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Args:
        card_number (str): Номер карты (16 цифр).

    Returns:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX.
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    masked = card_number[:6] + "*" * 6 + card_number[-4:]
    # Форматирование: XXXX XX** **** XXXX
    return f"{masked[:4]} {masked[4:6]}** **** {masked[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета.

    Args:
        account_number (str): Номер счета.

    Returns:
        str: Замаскированный номер в формате **XXXX.
    """
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать минимум 4 цифры.")

    return "**" + account_number[-4:]

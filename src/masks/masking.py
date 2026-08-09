import logging
import os

# --- Настройка логера модуля masks ---
os.makedirs("logs", exist_ok=True)

masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Args:
        card_number (str): Номер карты (16 цифр).

    Returns:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX.
    """
    if len(card_number) != 16 or not card_number.isdigit():
        masks_logger.error("Некорректный номер карты: длина=%d", len(card_number))
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    masked = card_number[:6] + "*" * 6 + card_number[-4:]
    result = f"{masked[:4]} {masked[4:6]}** **** {masked[-4:]}"
    masks_logger.info("Номер карты успешно замаскирован")
    return result


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета.

    Args:
        account_number (str): Номер счета.

    Returns:
        str: Замаскированный номер в формате **XXXX.
    """
    if len(account_number) < 4 or not account_number.isdigit():
        masks_logger.error(
            "Некорректный номер счета: длина=%d", len(account_number)
        )
        raise ValueError("Номер счета должен содержать минимум 4 цифры.")

    result = "**" + account_number[-4:]
    masks_logger.info("Номер счета успешно замаскирован")
    return result

import json
import logging
import os
from typing import Any, Dict, List

# --- Настройка логера модуля utils ---
os.makedirs("logs", exist_ok=True)

utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)


def read_operations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает список банковских операций из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с данными об операциях.

    Returns:
        Список словарей с операциями. Если файл не найден, пуст,
        повреждён или содержит не список — возвращается пустой список.
    """
    utils_logger.debug("Попытка чтения файла: %s", file_path)

    if not os.path.exists(file_path):
        utils_logger.error("Файл не найден: %s", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except (json.JSONDecodeError, OSError) as exc:
        utils_logger.error("Ошибка чтения файла %s: %s", file_path, exc)
        return []

    if not isinstance(data, list):
        utils_logger.error("Содержимое файла %s не является списком", file_path)
        return []

    utils_logger.info("Успешно прочитано %d операций из %s", len(data), file_path)
    return data

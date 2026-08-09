import json
import os
from typing import Any, Dict, List


def read_operations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает список банковских операций из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с данными об операциях.

    Returns:
        Список словарей с операциями. Если файл не найден, пуст,
        повреждён или содержит не список — возвращается пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return data

import os
from typing import Any, Dict, List, cast

import pandas as pd


def read_operations_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу с данными об операциях.

    Returns:
        Список словарей с операциями. Если файл не найден, пуст
        или повреждён — возвращается пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        dataframe = pd.read_csv(file_path, sep=";")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        return []

    records = cast(List[Dict[str, Any]], dataframe.to_dict(orient="records"))
    return records


def read_operations_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (XLSX).

    Args:
        file_path: Путь к XLSX-файлу с данными об операциях.

    Returns:
        Список словарей с операциями. Если файл не найден, пуст
        или повреждён — возвращается пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        dataframe = pd.read_excel(file_path)
    except (ValueError, OSError):
        return []

    records = cast(List[Dict[str, Any]], dataframe.to_dict(orient="records"))
    return records

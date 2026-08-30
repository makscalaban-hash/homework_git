import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
EXCHANGE_RATES_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли.

    Если валюта транзакции — RUB, обращение к внешнему API не происходит
    и сумма возвращается как есть. Для USD и EUR сумма конвертируется
    по текущему курсу через Exchange Rates Data API.

    Args:
        transaction: Словарь с данными транзакции. Ожидается структура
            {"operationAmount": {"amount": ..., "currency": {"code": ...}}}.

    Returns:
        Сумма операции в рублях, тип float.
    """
    operation_amount = transaction["operationAmount"]
    amount = float(operation_amount["amount"])
    currency_code = operation_amount["currency"]["code"]

    if currency_code == "RUB":
        return amount

    response = requests.get(
        EXCHANGE_RATES_URL,
        params={"to": "RUB", "from": currency_code, "amount": amount},
        headers={"apikey": API_KEY},
    )
    response.raise_for_status()
    result = response.json()["result"]

    return float(result)

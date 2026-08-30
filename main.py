import os
from typing import Any, Dict, List

from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.readers import read_operations_from_csv, read_operations_from_excel
from src.utils import read_operations_from_json
from src.widget import get_date, mask_account_card


def get_data_by_choice() -> List[Dict[str, Any]]:
    """Приветствует пользователя и запрашивает тип файла для обработки."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nВаш выбор: ").strip()

    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        return read_operations_from_json(os.path.join("data", "operations.json"))
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        return read_operations_from_csv(os.path.join("data", "transactions.csv"))
    elif choice == "3":
        print("\nДля обработки выбран XLSX-файл.")
        return read_operations_from_excel(
            os.path.join("data", "transactions_excel.xlsx")
        )
    else:
        print("\nНекорректный выбор. Попробуйте снова.\n")
        return get_data_by_choice()


def get_valid_status() -> str:
    """Запрашивает статус операций с валидацией ввода."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        user_status = input("\nВаш выбор: ").strip().upper()

        if user_status in valid_statuses:
            print(f'\nОперации отфильтрованы по статусу "{user_status}"')
            return user_status

        print(f'\nСтатус операции "{user_status}" недоступен.')


def _is_rub_transaction(transaction: Dict[str, Any]) -> bool:
    """Проверяет, что транзакция выполнена в рублях."""
    if transaction.get("currency_code") == "RUB":
        return True
    if transaction.get("currency_name") == "руб.":
        return True
    operation_amount = transaction.get("operationAmount")
    if isinstance(operation_amount, dict):
        return bool(operation_amount.get("currency", {}).get("code") == "RUB")
    return False


def print_formatted_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит итоговый список транзакций в требуемом виде."""
    if not transactions:
        print(
            "\nНе найдено ни одной транзакции, подходящей под ваши "
            "условия фильтрации"
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for item in transactions:
        date_str = get_date(str(item.get("date", "")))
        description = item.get("description", "Без описания")

        from_info = item.get("from")
        to_info = item.get("to")
        from_masked = mask_account_card(str(from_info)) if from_info else ""
        to_masked = mask_account_card(str(to_info)) if to_info else ""

        route = ""
        if from_masked and to_masked:
            route = f"{from_masked} -> {to_masked}"
        elif to_masked:
            route = to_masked
        elif from_masked:
            route = from_masked

        amount = item.get("amount")
        currency = item.get("currency_code") or item.get("currency_name")

        if isinstance(item.get("operationAmount"), dict):
            op_amount = item["operationAmount"]
            amount = op_amount.get("amount")
            currency = op_amount.get("currency", {}).get("name")

        print(f"{date_str} {description}")
        if route:
            print(route)
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """Основная функция программы."""
    transactions = get_data_by_choice()
    status = get_valid_status()

    # 1. Фильтрация по статусу
    transactions = filter_by_state(transactions, status)

    # 2. Сортировка по дате
    sort_choice = input(
        "\nОтсортировать операции по дате? Да/Нет\n"
    ).strip().lower()
    if sort_choice == "да":
        order_choice = input(
            "Отсортировать по возрастанию или по убыванию?\n"
        ).strip().lower()
        ascending = order_choice == "по возрастанию"
        transactions = sort_by_date(transactions, reverse=not ascending)

    # 3. Рублевые транзакции
    rub_choice = input(
        "\nВыводить только рублевые транзакции? Да/Нет\n"
    ).strip().lower()
    if rub_choice == "да":
        transactions = [t for t in transactions if _is_rub_transaction(t)]

    # 4. Фильтрация по слову в описании
    search_choice = input(
        "\nОтфильтровать список транзакций по определенному слову "
        "в описании? Да/Нет\n"
    ).strip().lower()
    if search_choice == "да":
        search_word = input("Введите слово для поиска:\n").strip()
        transactions = process_bank_search(transactions, search_word)

    # 5. Печать результата
    print("\nРаспечатываю итоговый список транзакций...")
    print_formatted_transactions(transactions)


if __name__ == "__main__":
    main()

# Виджет банковских операций

Проект для обработки и отображения последних банковских операций клиента.

## Цель проекта

Разработать набор функций для обработки данных о банковских операциях клиента:
маскирование номеров карт и счетов, фильтрация операций по статусу и сортировка
по дате — с последующим использованием этих функций в виджете, отображающем
последние операции клиента.

## Функциональность

- Маскирование номеров банковских карт и счетов
- Фильтрация операций по статусу (`filter_by_state`)
- Сортировка операций по дате (`sort_by_date`)
- Форматирование дат
- Работа с генераторами для эффективной обработки больших объёмов данных
  - Фильтрация транзакций по валюте (`filter_by_currency`)
  - Получение описаний транзакций (`transaction_descriptions`)
  - Генерация номеров банковских карт (`card_number_generator`)

## Установка и запуск

```bash
# Клонировать репозиторий
git clone <ваш_репозиторий>

# Установить зависимости (линтеры + тесты)
poetry install --with lint,test

# Запуск проверок
poetry run black --check src/
poetry run isort --check-only src/
poetry run flake8 src/
poetry run mypy src/
```

## Тестирование

Тесты написаны с использованием `pytest`, лежат в директории `tests/` — по одному
файлу на каждый тестируемый модуль (`test_masking.py`, `test_widget.py`,
`test_processing.py`), с общими фикстурами в `tests/conftest.py`. Для проверки
разных входных данных активно используется параметризация (`@pytest.mark.parametrize`).

```bash
# Запустить все тесты
poetry run pytest

# Запустить тесты с отчетом покрытия в терминале
poetry run pytest --cov=src --cov-report=term-missing

# Сгенерировать HTML-отчет покрытия (появится папка htmlcov/)
poetry run pytest --cov=src --cov-report=html
```

Открыть отчет о покрытии можно, открыв файл `htmlcov/index.html` в браузере.

## Примеры использования

```python
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Фильтрация
executed_ops = filter_by_state(operations)

# Сортировка (по убыванию)
sorted_ops = sort_by_date(operations)
```

### Работа с генераторами

```python
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

transactions = [
    {
        'id': 1,
        'description': 'Payment for services',
        'operationAmount': {'amount': '1000',
                             'currency': {'code': 'USD'}},
    },
    {
        'id': 2,
        'description': 'Transfer to friend',
        'operationAmount': {'amount': '5000',
                             'currency': {'code': 'RUB'}},
    },
]

# Фильтрация по валюте (возвращает итератор)
usd_transactions = filter_by_currency(transactions, 'USD')
for transaction in usd_transactions:
    print(transaction)

# Получение описаний транзакций (генератор)
descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)

# Генерация номеров карт
for card_number in card_number_generator(1, 5):
    print(card_number)
# Выведет:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...
```

## Структура проекта

- `src/masks/` — функции маскирования
- `src/widget.py` — виджеты
- `src/processing.py` — обработка данных
- `src/generators.py` — генераторы для работы с транзакциями
- `tests/` — тесты (pytest, фикстуры в `conftest.py`, отдельный файл теста на каждый модуль)
- `htmlcov/` — HTML-отчет о покрытии тестами (генерируется командой из раздела «Тестирование»)

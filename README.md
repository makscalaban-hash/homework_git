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

## Установка и запуск

```bash
# Клонировать репозиторий
git clone <ваш_репозиторий>

# Установить зависимости
poetry install --with lint

# Запуск проверок
poetry run black --check src/
poetry run isort --check-only src/
poetry run flake8 src/
poetry run mypy src/
```

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

## Структура проекта

- `src/masks/` — функции маскирования
- `src/widget.py` — виджеты
- `src/processing.py` — обработка данных
- `tests/` — тесты (будут добавлены позже)

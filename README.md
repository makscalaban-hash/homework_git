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
- Логирование работы модулей `masks` и `utils` (файлы в `logs/`)
- Чтение операций из JSON-файла (`read_operations_from_json`)
- Конвертация суммы операции в рубли, USD/EUR через внешний API (`convert_to_rub`)
- Чтение операций из CSV-файла (`read_operations_from_csv`)
- Чтение операций из Excel-файла (`read_operations_from_excel`)

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
from src.readers import read_operations_from_csv, read_operations_from_excel

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Фильтрация
executed_ops = filter_by_state(operations)

# Сортировка (по убыванию)
sorted_ops = sort_by_date(operations)

# Чтение из CSV / Excel
csv_ops = read_operations_from_csv("data/transactions.csv")
excel_ops = read_operations_from_excel("data/transactions_excel.xlsx")
```

## Структура проекта

- `src/masks/` — функции маскирования (с логированием)
- `src/widget.py` — виджеты
- `src/processing.py` — обработка данных
- `src/utils.py` — чтение операций из JSON (с логированием)
- `src/external_api.py` — конвертация валют через внешний API
- `src/readers.py` — чтение операций из CSV и Excel
- `tests/` — тесты (pytest, фикстуры в `conftest.py`, отдельный файл теста на каждый модуль)
- `logs/` — файлы логов модулей `masks` и `utils` (не в git)
- `htmlcov/` — HTML-отчет о покрытии тестами (генерируется командой из раздела «Тестирование»)

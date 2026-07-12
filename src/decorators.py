import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования работы функции.

    Логирует начало и конец выполнения функции, её результаты или ошибки.
    Может выводить логи в файл или консоль.

    Args:
        filename: Опциональное имя файла для записи логов. Если не задано,
            логи выводятся в консоль.

    Returns:
        Функция-декоратор.

    Example:
        @log(filename="mylog.txt")
        def my_function(x, y):
            return x + y

        my_function(1, 2)  # Запишет в mylog.txt: "my_function ok"
    """

    def decorator(func: Callable) -> Callable:
        """Внутренний декоратор, оборачивающий функцию."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка функции с логированием."""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result
            except Exception as e:
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(error_message, filename)
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """Вспомогательная функция для записи логов.

    Args:
        message: Сообщение для логирования.
        filename: Имя файла. Если None, выводит в консоль.
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)

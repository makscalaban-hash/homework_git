import pytest

from src.decorators import log


class TestLogDecoratorConsole:
    """Тесты логирования в консоль."""

    def test_logs_successful_execution(self, capsys):  # type: ignore
        """Проверяет логирование успешного выполнения функции."""

        @log()
        def add(x: int, y: int) -> int:
            return x + y

        result = add(2, 3)
        captured = capsys.readouterr()

        assert result == 5
        assert "add ok" in captured.out

    def test_logs_function_name_on_success(self, capsys):  # type: ignore
        """Проверяет, что в логе указано имя функции при успехе."""

        @log()
        def multiply(x: int, y: int) -> int:
            return x * y

        multiply(3, 4)
        captured = capsys.readouterr()

        assert "multiply ok" in captured.out

    def test_logs_error_with_exception_type(self, capsys):  # type: ignore
        """Проверяет логирование ошибки с типом исключения."""

        @log()
        def divide(x: int, y: int) -> float:
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out

    def test_logs_error_with_inputs(self, capsys):  # type: ignore
        """Проверяет логирование входных параметров при ошибке."""

        @log()
        def failing_func(a: int, b: int) -> int:
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_func(1, 2)

        captured = capsys.readouterr()
        assert "failing_func error: ValueError" in captured.out
        assert "Inputs: (1, 2), {}" in captured.out

    def test_logs_error_with_kwargs(self, capsys):  # type: ignore
        """Проверяет логирование kwargs при ошибке."""

        @log()
        def failing_with_kwargs(a: int, b: int = 2) -> int:
            raise RuntimeError("Test error with kwargs")

        with pytest.raises(RuntimeError):
            failing_with_kwargs(1, b=3)

        captured = capsys.readouterr()
        assert "failing_with_kwargs error: RuntimeError" in captured.out
        assert "Inputs: (1,), {'b': 3}" in captured.out

    @pytest.mark.parametrize(
        "args, kwargs",
        [
            ((5, 10), {}),
            ((1, 2, 3), {}),
            ((10,), {"x": 20}),
        ],
    )
    def test_logs_various_argument_combinations(
        self, capsys, args, kwargs  # type: ignore
    ) -> None:
        """Проверяет логирование различных комбинаций аргументов."""

        @log()
        def func_with_args(*args, **kwargs):  # type: ignore
            raise Exception("Test")

        with pytest.raises(Exception):
            func_with_args(*args, **kwargs)

        captured = capsys.readouterr()
        assert "func_with_args error:" in captured.out


class TestLogDecoratorFile:
    """Тесты логирования в файл."""

    def test_logs_to_file_on_success(self, temp_log_file: str) -> None:
        """Проверяет логирование в файл при успехе."""

        @log(filename=temp_log_file)
        def add(x: int, y: int) -> int:
            return x + y

        result = add(5, 3)
        assert result == 8

        with open(temp_log_file, "r") as f:
            log_content = f.read()

        assert "add ok" in log_content

    def test_logs_to_file_on_error(self, temp_log_file: str) -> None:
        """Проверяет логирование в файл при ошибке."""

        @log(filename=temp_log_file)
        def divide(x: int, y: int) -> float:
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        with open(temp_log_file, "r") as f:
            log_content = f.read()

        assert "divide error: ZeroDivisionError" in log_content
        assert "Inputs: (10, 0), {}" in log_content

    def test_appends_to_file(self, temp_log_file: str) -> None:
        """Проверяет, что логи добавляются в конец файла."""

        @log(filename=temp_log_file)
        def func1(x: int) -> int:
            return x + 1

        @log(filename=temp_log_file)
        def func2(x: int) -> int:
            return x + 2

        func1(1)
        func2(2)

        with open(temp_log_file, "r") as f:
            log_content = f.read()

        assert "func1 ok" in log_content
        assert "func2 ok" in log_content
        lines = log_content.strip().split("\n")
        assert len(lines) == 2

    def test_logs_error_to_file_with_kwargs(
        self, temp_log_file: str
    ) -> None:
        """Проверяет логирование ошибки с kwargs в файл."""

        @log(filename=temp_log_file)
        def failing(a: int, b: int = 5) -> int:
            raise KeyError("Not found")

        with pytest.raises(KeyError):
            failing(10, b=20)

        with open(temp_log_file, "r") as f:
            log_content = f.read()

        assert "failing error: KeyError" in log_content
        assert "Inputs: (10,), {'b': 20}" in log_content


class TestLogDecoratorBehavior:
    """Тесты поведения декоратора."""

    def test_reraises_exception(self) -> None:
        """Проверяет, что декоратор пробрасывает исключение дальше."""

        @log()
        def failing_func() -> None:
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            failing_func()

    def test_preserves_function_metadata(self) -> None:
        """Проверяет, что декоратор сохраняет метаданные функции."""

        @log()
        def my_function(x: int) -> int:
            """Тестовая функция."""
            return x + 1

        assert my_function.__name__ == "my_function"
        assert "Тестовая функция" in my_function.__doc__

    def test_returns_function_result(self) -> None:
        """Проверяет, что функция возвращает правильный результат."""

        @log()
        def compute(x: int, y: int) -> int:
            return x * y + 10

        result = compute(3, 4)
        assert result == 22

    @pytest.mark.parametrize(
        "value",
        [42, "string", [1, 2, 3], {"key": "value"}, None],
    )
    def test_handles_various_return_types(self, value):  # type: ignore
        """Проверяет работу с различными типами возвращаемых значений."""

        @log()
        def return_value():  # type: ignore
            return value

        result = return_value()
        assert result == value

    def test_multiple_calls_to_decorated_function(
        self, capsys
    ) -> None:  # type: ignore
        """Проверяет логирование при нескольких вызовах функции."""

        @log()
        def increment(x: int) -> int:
            return x + 1

        increment(1)
        increment(2)
        increment(3)

        captured = capsys.readouterr()
        output_lines = [
            line for line in captured.out.split("\n") if line.strip()
        ]
        assert len(output_lines) == 3
        assert all("increment ok" in line for line in output_lines)

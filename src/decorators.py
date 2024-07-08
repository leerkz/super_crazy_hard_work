import datetime
import typing
from functools import wraps


# Функция декоратора для логирования
def log(*, filename: str = "log_you_func") -> typing.Callable:
    """
    Декоратор, который записывает информацию о работе функции в файл лога.

    Args:
        filename (str): Имя файла для логирования. Если не указано, используется "log_you_func.log".
    """

    def wrapper(func: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:
        @wraps(func)
        def wrapped_func(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            # Попытка выполнить функцию
            try:
                result = func(*args, **kwargs)  # Вызов функции и получение результата
                log_result(filename, func.__name__, result)  # Запись успешного результата в лог
                return result  # Возврат результата функции
            except Exception as exception:
                log_exception(filename, func.__name__, exception)  # Запись исключения в лог
                raise  # Повторное возбуждение исключения

        return wrapped_func

    return wrapper


# Функция для записи успешного результата в лог
def log_result(filename: str, func_name: str, result: typing.Any) -> None:
    """
    Записывает успешный результат работы функции в файл лога.

    Args:
        filename (str): Имя файла для логирования.
        func_name (str): Имя функции.
        result (Any): Результат выполнения функции.
    """
    with open(f"{filename}.log", "a", encoding="utf8") as file:
        time_now = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")  # Текущее время
        file.write(f"{time_now} {func_name} ok\nresult: {result}\n{'=' * 50} passed {'=' * 50}\n")


# Функция для записи исключения в лог
def log_exception(filename: str, func_name: str, exception: Exception) -> None:
    """
    Записывает информацию об ошибке в файл лога.

    Args:
        filename (str): Имя файла для логирования.
        func_name (str): Имя функции.
        exception (Exception): Исключение, которое произошло при выполнении функции.
    """
    with open(f"{filename}.log", "a", encoding="utf8") as file:
        time_now = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")  # Текущее время
        file.write(
            f"{time_now} {func_name} error: {type(exception).__name__}\n"  # Запись типа ошибки
            f"full error: {exception}\n"  # Запись полного текста ошибки
            f"{'!' * 50}{type(exception).__name__}{'!' * 50}\n"  # Разделительная строка
        )

import json
import os.path

import pandas as pd

from src.reports import spending_by_category
from src.service import simple_find
from src.views import major


def main() -> None:
    # Приветственное сообщение для пользователя
    print("Главная")
    print("Введите дату в формате YYYY-MM-DD HH:MM:SS")
    date = input()

    # Вызов функции major и вывод результата
    result_major = major(date)
    print(json.loads(result_major))

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )

    # Поиск по ключевому слову
    print("Простой поиск")
    print("Введите строку которую надо найти в описании или категории")
    line = input()

    # Вызов функции simple_find и вывод результата
    result_simple_find = simple_find(line)
    print(json.loads(result_simple_find))

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )

    # Генерация отчета по выбранной категории
    print("Отчеты")
    print("Введите категорию по которой вы хотите увидеть отчеты")
    df = pd.read_excel(os.path.join("data", "operations.xls"))
    category = input()

    # Вызов функции spending_by_category и вывод результата
    result_spending_by_category = spending_by_category(df, category, date)
    print(result_spending_by_category)


if __name__ == "__main__":
    main()

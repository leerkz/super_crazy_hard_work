from datetime import datetime, timedelta

import pandas as pd

from src.config_log import setting_log

logger = setting_log("time_operations")


def greet_by_time_of_day(date_str: str) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    :param date_str: дата и время в формате YYYY-MM-DD HH:MM:SS
    :return: Приветствие в зависимости от времени суток
    """
    try:
        logger.info("Checking time of day...")
        date_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%H")
        if 4 <= int(date_object) <= 11:
            logger.info("Returning 'Good morning'")
            return "Доброе утро"
        elif 12 <= int(date_object) <= 16:
            logger.info("Returning 'Good afternoon'")
            return "Добрый день"
        elif 17 <= int(date_object) <= 23:
            logger.info("Returning 'Good evening'")
            return "Добрый вечер"
        elif 0 <= int(date_object) <= 3:
            logger.info("Returning 'Good night'")
            return "Доброй ночи"
        logger.info("Returning 'Welcome'")
        return "Добро пожаловать"
    except Exception as error:
        logger.error(f"Error: {error}")
        raise error


def generate_date_range(date_str: str, months: int = 1) -> list:
    """
    Генерирует диапазон дат на заданное количество месяцев назад.

    :param date_str: дата и время в формате YYYY-MM-DD HH:MM:SS
    :param months: количество месяцев для генерации диапазона
    :return: список дат в формате "M D Y"
    """
    try:
        logger.info("Generating date range...")
        base_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        date_list = []
        for _ in range(months):
            current_month = int(base_date.strftime("%m"))
            while int(base_date.strftime("%m")) == current_month:
                date_list.append(base_date.strftime("%m %d %Y"))
                base_date -= timedelta(days=1)
        logger.info(f"Generated date range: {date_list}")
        return date_list
    except Exception as error:
        logger.error(f"Error: {error}")
        raise error


def filter_operations_by_date_range(operations: list[dict], date_list: list) -> list[dict]:
    """
    Фильтрует операции по заданному диапазону дат.

    :param operations: список словарей с операциями
    :param date_list: список дат в формате "M D Y"
    :return: отфильтрованный список операций
    """
    try:
        filtered_list = []
        logger.info("Filtering operations by date range...")
        for item in operations:
            if item.get("Дата платежа"):
                formatted_date = datetime.strptime(item["Дата платежа"], "%d.%m.%Y").strftime("%m %d %Y")
                if formatted_date in date_list:
                    filtered_list.append(item)
        logger.info(f"Found {len(filtered_list)} operations within date range.")
        return filtered_list
    except Exception as error:
        logger.error(f"Error: {error}")
        raise error








def filter_dataframe_by_date_range(df: pd.DataFrame, date_list: list) -> pd.DataFrame:
    """
    Фильтрует строки датафрейма по заданному диапазону дат.

    :param df: датафрейм с операциями
    :param date_list: список дат в формате "M D Y"
    :return: отфильтрованный датафрейм
    """
    try:
        logger.info("Filtering dataframe by date range...")
        filtered_df = df[pd.to_datetime(df["Дата операции"], dayfirst=True).dt.strftime("%m %d %Y").isin(date_list)]
        logger.info("Filtered dataframe successfully.")
        return filtered_df
    except Exception as error:
        logger.error(f"Error: {error}")
        raise error
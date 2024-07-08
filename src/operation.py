from decimal import Decimal
from typing import Dict, List

import pandas as pd

from src.config_log import setting_log
from src.time import filter_operations_by_date_range, generate_date_range

logger = setting_log("operation")


def info_from_operation(operation: List[Dict[str, str]], date: str) -> List[Dict[str, str]]:
    """
    находит общую сумму всех операция по каждой карте
    :param operation: данные операций
    :param date: дата от которой идет отсчет
    :return: список с словарями с информацией о операциях по каждой карте
    """
    try:
        logger.info("find operation...")
        operation = filter_operations_by_date_range(operation, generate_date_range(date))

        info_card: Dict[str, Dict[str, Decimal]] = {}  # type annotation for info_card

        for item in operation:
            if int(item["Сумма операции"]) < 0:
                name = item["Номер карты"][-4:] if len(item["Номер карты"]) >= 4 else "Переводы"
                sum_operation = (
                    info_card.get(name, {"total_spent": Decimal(0), "cashback": Decimal(0)})["total_spent"]
                    + Decimal(item["Сумма операции"]) * -1
                )

                if sum_operation >= Decimal(100):
                    sum_cashback = info_card.get(name, {"total_spent": Decimal(0), "cashback": Decimal(0)})[
                        "cashback"
                    ] + Decimal(item["Сумма операции"]) * -1 / Decimal(100)
                    logger.info(f'sum operation: {str(item["Сумма операции"] * -1)} > 100 add cashback')
                else:
                    sum_cashback = info_card.get(name, {"total_spent": Decimal(0), "cashback": Decimal(0)})["cashback"]

                info_card[name] = {"total_spent": sum_operation, "cashback": sum_cashback}

        list_info: List[Dict[str, str]] = []
        for k, v in info_card.items():
            list_info.append(
                {
                    "last_digits": k,
                    "total_spent": str(info_card[k]["total_spent"]),
                    "cashback": str(info_card[k]["cashback"]),
                }
            )

        logger.info(f"create data count cart{len(list_info)}")
        return list_info

    except Exception as error:
        logger.error(f"operation error: {error}")
        raise error


def find_top_transactions(operation: list[dict], date: str, top: int = 5) -> list[dict]:
    """
    находит топ транзакий в диапозоне даты
    :param operation: данные операций
    :param date: дата
    :param top: число топов
    :return: список с топом операций
    """
    try:
        logger.info("getting operation...")
        operation = list(filter(lambda x: int(x["Сумма операции"]) < 0, operation))
        operation = filter_operations_by_date_range(operation, generate_date_range(date))

        top_list = []
        if top > len(operation):
            logger.info("user top > length operations")
            top = len(operation)

        for _ in range(top):
            leader = max(operation, key=lambda x: x["Сумма операции"] * -1)
            operation.remove(leader)

            top_list.append(
                {
                    "date": leader["Дата платежа"],
                    "amount": float(leader["Сумма операции"]) * -1,
                    "category": leader["Категория"],
                    "description": leader["Описание"],
                }
            )

            logger.info("new top find!")

        logger.info(f"top length: {len(top_list)}")
        return top_list

    except Exception as error:
        logger.error(f"error: {error}")
        raise error


def find_line(operation: list[dict], line: str) -> list[dict]:
    """находит словари с тем что поддал пользователь"""
    try:
        logger.info("getting operations...")
        new_data = [
            item
            for item in operation
            if line.lower() in item["Категория"].lower() or line.lower() in item["Описание"].lower()
        ]

        logger.info("find line!")
        return new_data

    except Exception as error:
        logger.error(f"error: {error}")
        raise error


def find_category_df(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    ищет строки с категориями
    :param df: датафрейм
    :param category: категория по которой идет поиск
    :return: отфильтрованный датафрейм
    """
    try:
        df = df[df["Категория"].str.lower() == category.lower()]
        logger.info("find done")
        return df

    except Exception as error:
        logger.error(f"error: {error}")
        raise error

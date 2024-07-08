from datetime import datetime
from typing import Optional

import pandas as pd

from src.config_log import setting_log
from src.operation import find_category_df
from src.time import filter_dataframe_by_date_range, generate_date_range

logger = setting_log("reports")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    возвращает траты по заданной категории за последние три месяца от переданной даты
    :param transactions: датафрейм операций
    :param category: категория
    :param date: дата если дата не подается то берется текущая
    :return: возвращает датафрейм
    """
    try:
        transactions = transactions[transactions["Сумма платежа"] < 0]

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"get current time: {date}")

        list_time = generate_date_range(date, 3)

        logger.info("finding category...")
        transactions = find_category_df(transactions, category)

        logger.info("filtering by time range...")
        transactions = filter_dataframe_by_date_range(transactions, list_time)

        logger.info("query complete")

        return transactions

    except Exception as error:
        logger.error(f"error: {error}")
        raise error

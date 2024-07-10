import json
import os
from pathlib import Path

from src.config_log import setting_log
from src.currency import get_currencies, get_sp500
from src.operation import find_top_transactions, info_from_operation
from src.time import greet_by_time_of_day
from src.utils import unpack_excel

logger = setting_log("views")


def major(date: str) -> str:
    """
    возвращает Json-ответ с информацией на главной
    :param date: дата
    :return: возвращает json-ответ
    """
    try:
        with open(os.path.join(Path(__file__).resolve().parents[1], "data/user_settings.json")) as f:
            logger.info("loading user settings...")
            info = json.load(f)

        logger.info("getting greeting...")
        greeting = greet_by_time_of_day(date)

        logger.info("unpacking operations...")
        data = unpack_excel(os.path.join(Path(__file__).resolve().parents[1], "data", "operations.xls"))

        logger.info("loading operations info...")
        list_operation = info_from_operation(data, date)

        logger.info("finding top transactions...")
        top = find_top_transactions(data, date)

        logger.info("getting currency rates...")
        list_currency = info["user_currencies"]
        currency = get_currencies(list_currency)

        logger.info("getting SP500 prices...")
        list_stocks = info["user_stocks"]
        sp500 = get_sp500(list_stocks)

        json_file = {
            "greeting": greeting,
            "cards": list_operation,
            "top_transactions": top,
            "currency_rates": currency,
            "stock_prices": sp500,
        }

        return json.dumps(json_file, ensure_ascii=False)

    except Exception as error:
        logger.error(f"error: {error}")
        raise error

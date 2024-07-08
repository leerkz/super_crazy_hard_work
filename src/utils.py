import os.path
from pathlib import Path

import pandas as pd
import requests

from src.config_log import setting_log

logger = setting_log("utils")


def write_xml_from_web(url: str, name: str) -> None:
    """
    записывает xml файл с сайта
    :param url: ссылка на сайт
    :param name: имя файла
    :return: None
    """
    try:
        logger.info("making request...")
        req = requests.get(url)
        logger.info("request successful")

        logger.info("writing xml file...")
        with open(os.path.join(Path(__file__).resolve().parents[1], "data", f"{name}.xml"), "wb") as file:
            file.write(req.content)
        logger.info("xml file written successfully")

    except Exception as error:
        logger.error(f"error: {error}")
        raise error


def unpack_excel(path: str) -> list:
    """распаковывает exel"""
    try:
        logger.info(f"unpacking excel from: {path}")
        formating_excel = pd.read_excel(path, na_filter=False)
        json_excel = formating_excel.to_dict(orient="records")
        logger.info("excel unpacked successfully")
        return json_excel

    except Exception as error:
        logger.error(f"unpack error: {error}")
        raise error

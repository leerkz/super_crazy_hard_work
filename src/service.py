import json
import os
from pathlib import Path

from src.config_log import setting_log
from src.operation import find_line
from src.utils import unpack_excel

logger = setting_log("service")


def simple_find(line: str) -> str:
    """
    Ищет операции с заданной категорией и возвращает результат в формате JSON.

    :param line: строка для поиска в описании или категории операций
    :return: JSON-строка с результатами поиска
    """
    try:
        logger.info("Starting simple find operation...")

        # Получаем путь к файлу с данными операций
        operations_file = os.path.join(Path(__file__).resolve().parents[1], "data", "operations.xls")

        # Распаковываем данные из Excel файла
        logger.info("Unpacking Excel file...")
        operation_data = unpack_excel(operations_file)

        # Ищем операции по заданной строке
        logger.info(f"Finding operations with line: '{line}'...")
        found_operations = find_line(operation_data, line)

        # Преобразуем результат в JSON
        logger.info("Preparing JSON response...")
        json_result = json.dumps(found_operations, ensure_ascii=False)

        logger.info("Simple find operation completed successfully.")
        return json_result

    except Exception as error:
        logger.error(f"Error in simple find operation: {error}")
        raise error

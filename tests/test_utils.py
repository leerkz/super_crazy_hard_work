import os.path
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from pandas import DataFrame
from src.utils import unpack_excel
from src.utils import write_xml_from_web


def test_write_xml_from_web() -> None:
    with patch("builtins.open") as mock_open, \
            patch("requests.get") as mock_get:
        time_now = datetime.strftime(datetime.now(), "%d/%m/%Y")
        url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={time_now}"

        write_xml_from_web(url, "cbr")

        expected_file_path = os.path.join(
            Path(__file__).resolve().parents[1], "data", "cbr.xml"
        )

        mock_open.assert_called_once_with(expected_file_path, "wb")
        mock_get.assert_called_once_with(url)


def test_unpack_excel() -> None:
    test_file_path = os.path.join("..", "data", "test.csv")

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = DataFrame({"test": ["test"]})

        result = unpack_excel(test_file_path)

        assert result == [{"test": "test"}]
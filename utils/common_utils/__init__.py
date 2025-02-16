"""Common utils"""

from json import JSONDecodeError, load
from typing import Any, List

import psutil

from utils.exceptions import UtilException

import os
import sys
new_work_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(new_work_dir)

from utils.custom_logger import CustomLogger

log_file_name = "common_utils.log"
logger_instance = CustomLogger(logger_name="common_utils",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,"logs", log_file_name),
                                level="info")
my_logger = logger_instance.logger

def load_json_from_file(file_path: str) -> Any:
    """Load json data from file"""

    with open(file_path, encoding="utf-8") as file:
            try:
                result = load(file)
            except JSONDecodeError as error:
                raise UtilException(
                    f"Файл {file_path} содержит ошибки в структуре json"
                ) from error

    return result


def write_lines_to_file(file_path: str, lines: List[str]) -> None:
    """write lines to file"""

    with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


def write_data_to_file(file_path: str, data: str) -> None:
    """write data to file"""

    with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)

def clear_temp_data():
    temp_file = os.path.join('tempdir', 'pid.txt')
    if os.path.isfile(temp_file):
        with open(temp_file, 'r') as pidfile:
            pid = int(pidfile.read())

    try:
        if not psutil.pid_exists(pid):
            os.remove(os.path.join('tempdir', 'pid.txt'))
    except Exception as err:
        my_logger.debug(err)
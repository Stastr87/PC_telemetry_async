"""Common utils"""
import re

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
                                level="debug")
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
    """Delete file pid.txt in tamp dir"""
    temp_file = os.path.join('tempdir', 'pid.txt')
    if os.path.isfile(temp_file):
        with open(temp_file, 'r') as pidfile:
            pid = int(pidfile.read())

    try:
        if not psutil.pid_exists(pid):
            os.remove(os.path.join('tempdir', 'pid.txt'))
    except Exception as err:
        my_logger.debug(err)

def temp_file_must_be_clean(func):
    """Clean temp file deco for flask response with send_file option"""
    def wrapper(*args):
        """makes magic"""
        resp = func(*args)
        headers = resp[0].headers
        cd = headers.getlist('Content-Disposition')
        file_name = cd[0].split('; ')[1]
        temp_file = re.sub('filename=', '', file_name)
        abs_temp_file = os.path.join(os.getcwd(),'tempdir', temp_file)
        with open (os.path.join(os.getcwd(),'tempdir','clean_file_list.txt'), 'a') as clean_file_list:
            clean_file_list.write('\n'+abs_temp_file)

        return resp
    return wrapper
"""Common utils"""

import os
import sys
from json import JSONDecodeError, load
from threading import Thread
from traceback import print_exc
from typing import Any, List

import psutil

from env.default_env import NEW_WORK_DIR

from utils.exceptions import UtilException
from utils.logger.custom_logger import CustomLogger

sys.path.append(NEW_WORK_DIR)

LOG_FILE_NAME = "common_utils.log"
logger_instance = CustomLogger(
    logger_name="common_utils",
    file_path=os.path.join(NEW_WORK_DIR, "logs", LOG_FILE_NAME),
    level="debug",
)
common_utils_logger = logger_instance.logger


class TestThread(Thread):
    """Customization of Thread class to run and handle possible exceptions"""

    def __init__(
        self,
        name: str,
        func: Any,
        *args,
        hello_msg: str = "",
        daemon: bool = False,
        **kwargs,
    ):
        super().__init__(name=name)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.test_exception = False
        self.daemon = daemon
        self.msg = hello_msg

    def run(self) -> None:
        """run method"""

        if self.msg:
            common_utils_logger.info("%s: %s", self.func.__name__, self.msg)
        else:
            common_utils_logger.info("%s started", self.func.__name__)

        try:
            self.func(**self.kwargs)

        except Exception as error:  # pylint: disable=W0718
            self.test_exception = True
            common_utils_logger.error(str(error), exc_info=True)
            print_exc()

    def join(self, timeout: float = None) -> None:
        """Join method"""

        super().join(timeout)
        common_utils_logger.info("%s Thread join method.", self.name)


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

    pid = 0
    temp_file = os.path.join("tempdir", "pid.txt")
    if os.path.isfile(temp_file):
        with open(temp_file, "r", encoding="utf8") as pid_file:
            pid = int(pid_file.read())

    try:
        if not psutil.pid_exists(pid):
            os.remove(os.path.join("tempdir", "pid.txt"))
    except OSError as err:
        common_utils_logger.debug(err)

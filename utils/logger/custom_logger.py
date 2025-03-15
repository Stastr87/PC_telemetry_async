"""Work with logging"""

import logging
import os.path
import sys
from logging import Formatter


def set_formatter(
    fmt_str: str = "[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
    dt_fmt: str = "%Y-%m-%d %H:%M:%S",
) -> Formatter:
    """Return datetime formatter for future actions"""
    return Formatter(fmt_str, datefmt=dt_fmt)


class CustomLogger:
    """
    Custom Logger

    Настройки могут быть выполнены при вызове CustomLogger
    индивидуально для каждого модуля, либо...
    Могут быть сохранены централизованно в ini файле
    Пример для импорта логера с централизованными настройками в модуль:
    ```
    import logging.configlogging.config.fileConfig('/path/to/logging.ini',
                                                   disable_existing_loggers=False)
    logger = logging.getLogger(name)
    ```
    """

    def __init__(
        self,
        logger_name: str,
        level: str = "DEBUG",
        file_path: str = "",
        mode: str = "w",
    ):
        self.logger = logging.getLogger(logger_name)
        self.formatter = set_formatter()
        self.level = level
        self.set_level()
        self.mode = mode
        self.file_path = file_path
        self.logger.handlers.clear()
        self.set_sh_formater()
        self.set_fh_formater()

    def get_logger(self):
        """Get logger"""
        return self.logger

    def set_level(self):
        """Set level"""
        if self.level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        if self.level.lower() == "error":
            self.logger.setLevel(logging.ERROR)
        if self.level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        if self.level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)
        if self.level.lower() == "critical":
            self.logger.setLevel(logging.CRITICAL)
        if not self.level:
            self.logger.setLevel(logging.NOTSET)

    def set_sh_formater(self):
        """
        Определяет формат вывода сообщений в консоль
        """
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(self.formatter)
        self.logger.addHandler(sh)

    def set_fh_formater(self):
        """
        Определяет формат вывода сообщений в файл
        """
        if self.file_path:
            if not os.path.isdir(os.path.dirname(self.file_path)):
                os.mkdir(os.path.dirname(self.file_path))

            fh = logging.FileHandler(
                filename=self.file_path, mode=self.mode, encoding="utf-8"
            )
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)

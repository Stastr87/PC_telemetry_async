"""Init temp file remover module"""

import time
from datetime import datetime, timedelta

from env.default_env import CLEAR_TEMP_FOLDER_TIMEOUT
from utils.common_logger import common_logger
from utils.temp_file_remover import del_temp_files


def file_remover():
    """Clean temp folder from old json files"""
    start = datetime.now()
    while True:

        if datetime.now() - start > timedelta(seconds=CLEAR_TEMP_FOLDER_TIMEOUT):
            removed_files, remove_file_error = del_temp_files()
            start = datetime.now()
            if removed_files:
                common_logger.debug('removed_files: %s', removed_files)
            if remove_file_error:
                common_logger.debug('remove_file_error: %s', remove_file_error)

        time.sleep(1)

if __name__ == "__main__":
    file_remover()

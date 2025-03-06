"""Init temp file remover module"""

import time
from datetime import datetime, timedelta

from env.default_env import CLEAR_TEMP_FOLDER_TIMEOUT
from utils.temp_file_remover import del_temp_files


def file_remover():
    """Clean temp folder from old json files"""
    start = datetime.now()
    print("Temp folder cleaner started.")
    while True:
        try:
            if datetime.now() - start > timedelta(seconds=CLEAR_TEMP_FOLDER_TIMEOUT):
                removed_files, remove_file_error = del_temp_files()
                start = datetime.now()
                print(
                    f"removed_files: {removed_files}",
                    f"remove_file_error: {remove_file_error}",
                )
        except KeyboardInterrupt:
            print("Keyboard Interrupt handed")
        time.sleep(1)


if __name__ == "__main__":
    file_remover()

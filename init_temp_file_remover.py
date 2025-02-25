"""Init temp file remover module"""

import sys
import time

from utils.temp_file_remover import del_temp_files

if __name__ == "__main__":
    while True:
        try:
            del_temp_files()
            time.sleep(300)
        except KeyboardInterrupt:
            IS_RUNNING = False
            sys.exit(0)

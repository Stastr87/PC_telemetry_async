import sys
import time

from utils.temp_file_remover import del_temp_files

if __name__ == '__main__':
    print('init temp file remover module')
    while True:
        try:
            del_temp_files()
            time.sleep(600)
        except KeyboardInterrupt:    #Без этой строчки код будет выполняться бесконечно при любом количестве ошибок
            is_running=False
            sys.exit(0)
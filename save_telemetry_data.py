import sys

import data_operation



if __name__ == '__main__':

    while True:
        try:
            data_operation.init_collect_hw_data()
        except KeyboardInterrupt:    #Без этой строчки код будет выполняться бесконечно при любом количестве ошибок
            is_running=False
            sys.exit(0)

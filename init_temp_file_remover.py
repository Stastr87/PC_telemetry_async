"""Init temp file remover module"""

import curses
import sys
import time
from datetime import datetime, timedelta

from env.default_env import CLEAR_TEMP_FOLDER_TIMEOUT
from utils.temp_file_remover import del_temp_files


def draw_file_remover(canvas):
    """Define CLI interface with info"""

    start = datetime.now()
    removed_files = []
    remove_file_error = []
    while True:
        try:
            # Очистка холста
            canvas.clear()

            # Запуск скрипта очистки временной директории
            if datetime.now() - start > timedelta(seconds=CLEAR_TEMP_FOLDER_TIMEOUT):
                removed_files, remove_file_error = del_temp_files()
                start = datetime.now()

            # Размещение строк в интерфейсе
            count_down = (
                timedelta(seconds=CLEAR_TEMP_FOLDER_TIMEOUT) - (datetime.now() - start)
            ).seconds
            rows = [
                "Press ESC to Exit...",
                f"for next delete temp files {count_down} sec.",
                f"removed_files: {removed_files}",
                f"remove_file_error: {remove_file_error}",
            ]

            # Отступ от края для визуального восприятия
            main_offset = 2
            # Добавить обновленные строки на холст
            for i, row in enumerate(rows):
                canvas.addstr(i + 1, main_offset, row)

            canvas.refresh()
            # Перехват нажатия клавиши
            if canvas.getch() == 27:
                curses.endwin()
                print("EXIT file_remover")
                sys.exit(0)

            # Холст обновляется с частотой 1Гц
            time.sleep(1)

        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    stdscr = curses.initscr()
    # Не показывать вводимые символы
    curses.noecho()
    # Активировать режим прерывания для возможности раеализация завершения программы
    curses.cbreak()
    # Обновление холста будет работать автоматически без ожидания нажатий клавиш
    stdscr.nodelay(True)
    # Отключить мигающий курсор
    curses.curs_set(False)

    curses.wrapper(draw_file_remover(stdscr))

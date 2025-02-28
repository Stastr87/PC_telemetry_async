"""Init temp file remover module"""

import curses
import sys
import time
from datetime import datetime, timedelta

from utils.temp_file_remover import del_temp_files


def draw(canvas):
    """Define CLI interface with info"""

    curses.noecho()
    curses.cbreak(True)
    # Обновление холста будет работать автоматически без ожидания нажатий клавиш
    canvas.nodelay(True)
    # Отключить мигающий курсор
    curses.curs_set(False)
    start = datetime.now()
    removed_files = []
    remove_file_error = []
    while True:
        try:
            canvas.clear()
            main_offset = 2
            canvas.refresh()
            canvas.nodelay(True)

            # Запуск скрипта очистки временной директории
            if datetime.now() - start > timedelta(seconds=15):
                removed_files, remove_file_error = del_temp_files()
                start = datetime.now()

            # Разместим в окне терминала строки интерфейса
            count_down = (timedelta(seconds=15) - (datetime.now() - start)).seconds
            rows = [
                "Press ESC to Exit...",
                f"for next delete temp files {count_down} sec.",
                f"removed_files: {removed_files}",
                f"remove_file_error: {remove_file_error}",
            ]

            for i, row in enumerate(rows):
                canvas.addstr(i + 1, main_offset, row)

            canvas.refresh()
            # Холст обновляется с частотой 1Гц
            time.sleep(1)

            key = canvas.getch()
            if key == 27:
                curses.nocbreak()
                canvas.keypad(False)
                curses.echo()
                # endwin - завершает сессию и возвращает в обычную консоль
                curses.endwin()
                print("EXIT")
                sys.exit(0)

        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)

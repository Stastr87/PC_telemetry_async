"""Saving telemetry data to local path"""

import curses
import socket
import sys
from curses import wrapper
from datetime import datetime, timezone

import data_operation


def draw_telemetry_data(canvas):
    """Define CLI interface with info"""
    display_result = "NO DATA"
    while True:
        try:
            # Очистка холста
            canvas.clear()

            # Размещение строк в интерфейсе
            cur_date_time = (
                datetime.now(timezone.utc).astimezone().strftime("%d-%m-%Y %H:%M:%S %z")
            )

            rows = [
                "Press ESC to Exit...",
                f"Host name: {socket.gethostname()}",
                f"Current date/time {cur_date_time}",
                f"{display_result}",
            ]
            # Отступ от края для визуального восприятия
            offset = 2

            # Добавить обновленные строки на холст
            for i, row in enumerate(rows):
                canvas.addstr(i + 1, offset, row)

            canvas.refresh()
            # Перехват нажатия клавиши
            if canvas.getch() == 27:
                # endwin - завершает сессию и возвращает в обычную консоль
                curses.endwin()
                print("EXIT saving telemetry data")
                sys.exit()

            # Код выполняется 5 сек. Частота обновления экрана 0,2 Гц
            display_result = data_operation.init_collect_hw_data_for_display()

        except KeyboardInterrupt:
            pass


def init_curses():
    """Init curses object"""

    # Инициализация библиотеки. Создает виртуальный экран
    stdscr = curses.initscr()
    # Не показывать вводимые символы
    curses.noecho()
    # Активировать режим прерывания для возможности раеализация завершения программы
    curses.cbreak()
    # Отключить мигающий курсор
    curses.curs_set(False)
    # Обновление холста будет работать автоматически без ожидания нажатий клавиш
    stdscr.nodelay(True)
    return stdscr


if __name__ == "__main__":
    canvas_obj = init_curses()
    wrapper(draw_telemetry_data(canvas_obj))

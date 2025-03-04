"""Init common curses object with common settings"""

import curses


def init_curses():
    """Init common curses object"""

    # Инициализация библиотеки. Создает виртуальный экран.
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

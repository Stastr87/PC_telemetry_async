import time
import curses
import random
from datetime import datetime
import csv
import os
from hardware_monitor import HardWareMonitor

def get_data_for_show():
    date = datetime.now().strftime('%d-%m-%Y')
    file_path = os.path.abspath(os.path.join('telemetry',date,'data.csv'))
    text_list = []
    with open(file_path, encoding='utf-8') as r_file:
        for line in r_file:
            line = line.split(",", 2)
            text_list.append(" ".join(line))
    return text_list

def get_hardware_telemerty():
    '''Сохраняет CSV файл с данными по потреблению ресурсов ПК
    
    Этот код выполняется 5 секунд, если не передано другое значение в класс HardWareMonitor()
    Параметр monitor_period=5
    '''
    # 
    data = HardWareMonitor()
    return round(data.ram_free), round(data.cpu_usage)

def draw(canvas):
    # Обычно приложения curses отключают автоматическое отображение клавиш на экране,
    # чтобы иметь возможность читать клавиши и отображать их только при определенных обстоятельствах. 
    # Для этого необходимо вызвать функцию noecho().
    curses.noecho()

    # Приложениям также обычно требуется мгновенно реагировать на клавиши, 
    # не требуя нажатия клавиши Enter; это называется режимом cbreak, 
    # в отличие от обычного режима ввода с буферизацией.
    curses.cbreak()
    
    while True:


        canvas.clear()
        canvas.border()
        # Отключить мигающий курсор
        curses.curs_set(False)
        row, column = (1, 1)
        canvas.addstr(row, column, datetime.now().strftime('%d-%m-%Y %H:%M:%S'),curses.A_BOLD)
        row, column = (2, 1)
        hw_data = get_hardware_telemerty()

        display_string = f'''Дата/время: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\nСвободная память RAM: {hw_data[0]} %\nНагрузка на ЦП: {hw_data[1]} %
        '''
        canvas.addstr(row, column, display_string)
        canvas.refresh()
        time.sleep(1)
        
        canvas.nodelay(True)
        key = canvas.getch()

        if key == 27:
            curses.nocbreak()
            canvas.keypad(False)
            curses.echo()
            # endwin - завершает сессию и возвращает в обычную консоль
            curses.endwin()
            print("EXIT")
            quit()


  
if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
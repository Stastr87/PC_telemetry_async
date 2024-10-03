import time
import curses
import random
from datetime import datetime
import csv
import os
from hardware_monitor import HardWareMonitor


def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent_value = 100*(iteration / float(total))
    percent = ("{0:." + str(decimals) + "f}").format(percent_value)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    bar_body = f'{prefix} |{bar}| {suffix}'

    return bar_body


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

# def set_styles():
#     ''' Применяет цветовые стили для модуля curses
#     '''
#     curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

def draw(canvas):
    # Обычно приложения curses отключают автоматическое отображение клавиш на экране,
    # чтобы иметь возможность читать клавиши и отображать их только при определенных обстоятельствах. 
    # Для этого необходимо вызвать функцию noecho().
    curses.noecho()

    # Приложениям также обычно требуется мгновенно реагировать на клавиши, 
    # не требуя нажатия клавиши Enter; это называется режимом cbreak, 
    # в отличие от обычного режима ввода с буферизацией.
    curses.cbreak()
    
    # Добавим набор стилей для отображения текста
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    while True:
        canvas.clear()
        canvas.border()
        # Отключить мигающий курсор
        curses.curs_set(False)
        hw_data = get_hardware_telemerty()
      
        
        normilize_str = lambda x: str(x) if len(str(x)) > 1 else f'0{x}'
        ram_data = hw_data[0]
        otput_ram_info_str = f'RAM usage (RAM free {normilize_str(ram_data)}%)'
        cpu_data = hw_data[1]
        cpu_info_ouput_str = f'CPU usage {normilize_str(cpu_data)}%'

        canvas.addstr(2, 2, otput_ram_info_str)
        canvas.addstr (2,len(otput_ram_info_str)+2, print_progress_bar(100-ram_data, 100, length=30))
        if ram_data<40:
            canvas.addstr(2, 2, otput_ram_info_str, curses.color_pair(1))
            canvas.addstr (2, len(otput_ram_info_str)+2, print_progress_bar(100-ram_data, 100, length=30))
        
        canvas.addstr(3, 2, cpu_info_ouput_str)
        canvas.addstr(3, len(otput_ram_info_str)+2, print_progress_bar(cpu_data, 100, length=30))
        if cpu_data>16:
            canvas.addstr(3, 2, cpu_info_ouput_str, curses.color_pair(1))
            canvas.addstr(3, len(otput_ram_info_str)+2, print_progress_bar(cpu_data, 100, length=30))
        
        canvas.addstr(1, 2, f'Current date/time')
        canvas.addstr(1, len(otput_ram_info_str)+3, datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

        canvas.refresh()
        # time.sleep(1)
        
        canvas.nodelay(True)
        key = canvas.getch()
        
        if key == 27:
            curses.nocbreak()
            canvas.keypad(False)
            curses.echo()
            # endwin - завершает сессию и возвращает в обычную консоль
            curses.endwin()
            print(f"EXIT")
            quit()


  
if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
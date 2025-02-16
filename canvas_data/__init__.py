import os, sys, socket

new_work_dir = os.path.abspath(os.path.join(__file__ ,"../.."))
sys.path.append(new_work_dir)
from datetime import datetime, timezone
from tabulate import tabulate
from async_hardware_monitor import HardWareMonitor
import data_operation


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


# def get_data_for_show():
#     date = datetime.now().strftime('%d-%m-%Y')
#     file_path = os.path.abspath(os.path.join('telemetry',date,'data.csv'))
#     text_list = []
#     with open(file_path, encoding='utf-8') as r_file:
#         for line in r_file:
#             line = line.split(",", 2)
#             text_list.append(" ".join(line))
#     return text_list

def get_hardware_telemetry()->tuple:
    """Сохраняет CSV файл с данными по потреблению ресурсов ПК

    Этот код выполняется 5 секунд, если не передано другое значение в класс HardWareMonitor()
    Параметр monitor_period=5

    return:
    ram_free - данные по свободной памяти ОЗУ, %
    cpu_usage - потребление ресурсов ЦП, %
    network_usage - словарь с данными по трафику на сетевых интерфейсах"""
    
    ram_free, cpu_usage, network_usage = None, None, None

    data = HardWareMonitor().to_dict()
    if (data['ram_free'] and 
        data['cpu_usage'] and
        data['network_usage']):
        network_usage = data['network_usage']
        
        # Сохраняем данные в CSV
        data_operation.create_telemetry_data()
        data_operation.update_telemetry_data_v2(data)
        
        ram_free, cpu_usage, network_usage = (round(data['ram_free']), 
                                              round(data['cpu_usage']), 
                                              network_usage)
    
    return ram_free, cpu_usage, network_usage

def get_canvas_data()->dict:
    """Формирует данные для отображения в консоли

    return:
    display_map - словарь со строками данных"""
    
    pc_name = f'Host name: {socket.gethostname()}' # Получим имя ПК
    cur_date_time = f"Current date/time {datetime.now(timezone.utc).astimezone().strftime('%d-%m-%Y %H:%M:%S %z')}"
    # cur_date_time = f"Current date/time {datetime.now(timezone.utc).astimezone().isoformat()}"
    
    ram_data, cpu_data, network_usage_data = get_hardware_telemetry()
    # print(f'get_canvas_data() -> {ram_data, cpu_data, network_usage_data}')
        
    if not ram_data:
        ram_data = 0
    
    #Подготавливаем строки для отображения на холсте
    normalize_str = lambda x: str(x) if len(str(x)) > 1 else f'0{x}'
    output_ram_info_str = f'RAM usage (RAM free {normalize_str(ram_data)}%)   {print_progress_bar(100-ram_data, 100, length=30)}'
        
    if not cpu_data:
        cpu_data = 0
    
    cpu_info_output_str = f'CPU usage {normalize_str(cpu_data)}%              {print_progress_bar(cpu_data, 100, length=30)}'
        
    if network_usage_data:
        network_info = []
        for net_adapter in network_usage_data:
            if network_usage_data[net_adapter]['up']>1 or network_usage_data[net_adapter]['down']:
                network_info.append([net_adapter,
                                     round(network_usage_data[net_adapter]['down']*0.000008,2),
                                     round(network_usage_data[net_adapter]['up']*0.000008,2)])
        # Создаим таблицу для отображения данных сетевых интерфейсов
        headers = ['Net adater', 'DOWNLOAD, Mbit/sec', 'UPLOAD, Mbit/sec']
        net_adapters_table_object = tabulate(network_info, headers, tablefmt="github")
        # Условно разделим холст на блоки 
        display_map={"pc_name": pc_name, 
                     "cur_date_time":cur_date_time,
                     "ram_info":output_ram_info_str,
                     "cpu_info":cpu_info_output_str,
                     "net_usage":net_adapters_table_object
                    }
        # Если данные по сети не получены, то исключаем их из списка блоков
        if not network_usage_data:
            display_map={"pc_name": pc_name, 
                         "cur_date_time":cur_date_time,
                         "ram_info":output_ram_info_str,
                         "cpu_info":cpu_info_output_str,
                        }
     
        return display_map

def get_txt():
    """Возвращает данные в виде строк"""

    data_map = get_canvas_data()
    txt = str()
    for block in data_map:
          txt+=data_map[block]+'\n\n'
    return txt
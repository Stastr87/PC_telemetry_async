import json
import os
from datetime import datetime, timezone
import time
import csv
from pprint import pprint

from async_hardware_monitor import HardWareMonitor
from utils.custom_logger import CustomLogger
import os
import sys
new_work_dir = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(new_work_dir)
log_file_name = "data_operation.log"
logger_instance = CustomLogger(logger_name="data_operation",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,"logs", log_file_name),
                                level="debug")
my_logger = logger_instance.logger

def init_collect_hw_data():
    """Сохраняет CSV файл с данными по потреблению ресурсов ПК

        Этот код выполняется 5 секунд, если не передано другое значение в класс HardWareMonitor()
        Параметр monitor_period=5"""

    data = HardWareMonitor().to_dict()
    # my_logger.debug(f'init_collect_hw_data() -> data:\n{json.dumps(data, indent=4, ensure_ascii=False).encode('utf8')}')
    pprint(data)
    # Сохраняем данные в CSV
    create_telemetry_data()
    update_telemetry_data_v2(data)



def create_telemetry_data(data_file='data.csv'):
    """Create empty csv file
    """
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name,data_file)
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # Таймер для того что бы создалась директория
        time.sleep(0.2)
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'cpu_usage', 'ram_free','network_adapter','net_usage_up','net_usage_down'])


def update_telemetry_data_v2(data : dict, file_name: str = 'data.csv'):
    """ Add data to *.csv file

    arguments:
    data - hardware usage data
    file_name - *.csv file name
    """
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name, file_name)
    
    # Если папка существует, но в ней нет файла, то его нужно создать с указанной шапкой
    if not os.path.exists(file_path):
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'cpu_usage', 'ram_free','network_adapter','net_usage_up','net_usage_down'])

    with open(file_path, mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
        for net_adaptor in list(data['network_usage'].keys()):
            file_writer.writerow([datetime.now().astimezone().isoformat(),
                                  round(float(data['cpu_usage'])),
                                  round(float(data['ram_free'])),
                                  net_adaptor,
                                  round(float(data['network_usage'][net_adaptor]["up"])),
                                  round(float(data['network_usage'][net_adaptor]["down"]))])

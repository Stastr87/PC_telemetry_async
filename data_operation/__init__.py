import os
from datetime import datetime
import time
import csv



def create_telemerty_data():
    '''Создает пустой CSV файл в пепке хранения телеметрии
    '''
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name,'data.csv')
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # Таймер для того что бы создалась директория
        time.sleep(0.2)
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'cpu_usage', 'ram_free','network_adapter','net_usage_up','net_usage_down'])

def update_telemerty_data(data):
    ''' Добавляет данные в существующий CSV файл
    '''
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name,'data.csv')

    with open(file_path, mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
        for net_adaptor in list(data.network_usage.keys()):
            file_writer.writerow([datetime.now(),
                                  round(float(data.cpu_usage)),
                                  round(float(data.ram_free)),
                                  net_adaptor,
                                  round(float(data.network_usage[net_adaptor]["up"])),
                                  round(float(data.network_usage[net_adaptor]["down"]))])

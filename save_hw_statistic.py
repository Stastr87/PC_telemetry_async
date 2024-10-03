import logging
import csv
from hardware_monitor import HardWareMonitor
from roperator_monitor import RoperatorMonitor
import data_operation
from pprint import pprint

import logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s] %(message)s'
                    # filename="log/hardware_statistic.log",
                    # filemode="a"
                    )

def log_hardware_telemerty():
    '''Сохраняет CSV файл с данными по потреблению ресурсов ПК
    
    Этот код выполняется 5 секунд, если не передано другое значение в класс HardWareMonitor()
    Параметр monitor_period=5
    '''
    # 
    data = HardWareMonitor()
    logging.info(f'ram_free {round(data.ram_free)}%; cpu_usage {round(data.cpu_usage)}%')
    print( f'network_usage {data.network_usage}')
    data_operation.create_telemerty_data()
    data_operation.update_telemerty_data(data)

def log_recording_channels(monitor_obj):
    '''Сохраняет CSV файл с данными по потреблению ресурсов ПК
    '''
    monitor = monitor_obj
    returned_data = monitor.get_channel_recordings()

    # Составим список статусов по каналам устройств
    recording_data = []
    for channel in returned_data['channels']:
        device_name = monitor.get_device_name(channel['channel'])
        recording_data.append((device_name, channel['status']['recordStatus']['error']['isError']))
    
    print( f'recording_data: {recording_data}')
    data_operation.create_channel_record_data()
    data_operation.update_channel_record_data(recording_data)


if __name__ == '__main__':
    # За рамки цикла необходимо вынести авторизацию для того что бы сервер оператора не перегружался бесполезными сессиями
    monitor_obj = RoperatorMonitor()
    try:
        while True:
            log_hardware_telemerty()
            log_recording_channels(monitor_obj)
    
    except KeyboardInterrupt:
        # В случае какого либо исключения завершить сессию подключения к серверу Оператор
        monitor_obj.close_connection()
        logging.info('Логирование телеметрии завершено', exc_info=True)
    
    except Exception as e:
        monitor_obj.close_connection()
        logging.error('Логирование телеметрии завершено ошибкой', exc_info=True)







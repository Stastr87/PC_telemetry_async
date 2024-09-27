import logging
import csv
from hardware_monitor import HardWareMonitor
import data_operation

import logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    filename="log/hardware_statistic.log",
                    filemode="a")

if __name__ == '__main__':
    while True:
        data = HardWareMonitor()
        print(f'ram_free {data.ram_free}', f'cpu_usage {data.cpu_usage}', f'network_usage {data.network_usage}')
        data_operation.create_telemerty_data()
        data_operation.update_telemerty_data(data)





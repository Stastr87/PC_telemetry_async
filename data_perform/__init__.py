import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    filename="log/hardware_statistic.log",
                    filemode="a")



def create_data_frame():
    folder_name = os.path.abspath(os.path.join('telemetry','25-09-2024'))
    file_path = os.path.join(folder_name,'data.csv')
    columns=['time', 'cpu_usage', 'ram_free','network_adapter','net_usage_up','net_usage_down']
    newDataFrame=pd.DataFrame(columns=columns)
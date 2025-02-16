"""
Модуль для работы с сохраненными данными
"""
import json
import os
import sys
from datetime import datetime
import csv

import pandas as pd

new_work_dir = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(new_work_dir)

from utils.custom_logger import CustomLogger

log_file_name = "return_hw_statistic.log"
logger_instance = CustomLogger(logger_name="stored_data_operation",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,"logs", log_file_name),
                                level="debug")

my_logger = logger_instance.logger


class DataObject:
    def __init__(self, start_time: str, end_time: str):
        self.start_time = start_time
        self.end_time = end_time
        self._dt_start = datetime.fromisoformat(self.start_time)
        self._dt_end = datetime.fromisoformat(self.end_time)


    def get_temp_data_frame(self):
        """Return temp data frame according requested time period"""
        data_path = os.path.abspath(os.path.join(new_work_dir, 'telemetry'))
        dir_list = os.listdir(data_path)
        # Запишем данные во временный массив
        temp_data = []
        for dir_name in dir_list:
            stored_date = datetime.strptime(dir_name, '%d-%m-%Y')
            # Находим начальную дату
            if stored_date.date() >= self._dt_start.date():
                # Читаем csv файл и преобразуем в DataFrame
                df = pd.read_csv(os.path.join(data_path, dir_name, 'data.csv'))
                temp_data.append(df)
            if stored_date.date() > self._dt_end.date():
                break
        # Объединяем и возвращаем полученный DataFrame
        result = pd.concat(temp_data)
        # ТУТ ЕЩЕ НАДО ОТФИЛЬТРОВАТЬ ПО ВРЕМЕНИ

        return result


    def get_cpu_usage(self):
        """Return cpu usage data from temp DataFrame"""
        df = self.get_temp_data_frame()
        cpu_df = df[['time', 'cpu_usage']]
        return cpu_df.values.tolist()

    def get_csv_data(self):
        """Return all hardware usage data according requested time period"""
        data_path = os.path.abspath(os.path.join(new_work_dir, 'telemetry'))
        dir_list = os.listdir(data_path)

        # Запишем данные во временный массив
        temp_data = ''
        for dir_name in dir_list:
            stored_date = datetime.strptime(dir_name, '%d-%m-%Y')
            # Находим начальную дату
            if stored_date.date() >= self._dt_start.date():
                # Читаем csv файл
                with open(os.path.join(data_path, dir_name, 'data.csv'),
                          # newline='',
                          encoding="utf-8") as csvfile:
                    data_reader = csv.reader(csvfile,
                                             delimiter=",",
                                             lineterminator="\r",)
                    next(data_reader, None) # Skip headers
                    # Записываем во временный массив данные за промежуток времени указанный в запросе
                    for row in data_reader:
                        if datetime.fromisoformat(row[0]).time() >= self._dt_start.time():
                            temp_data+=str(row).replace("[","").replace("]","")+f"\n"
                            temp_data = temp_data.replace(" ", '')
                        if datetime.fromisoformat(row[0]).astimezone() >= self._dt_end.astimezone():
                            break


            if stored_date.date() > self._dt_end.date():
                break



        return temp_data

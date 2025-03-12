"""Stored data operations"""

import csv
import os
import sys
from datetime import datetime

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from env.default_env import NEW_WORK_DIR
from utils.custom_logger import CustomLogger

sys.path.append(NEW_WORK_DIR)

LOG_FILE_NAME = "stored_data_operation.log"
logger_instance = CustomLogger(
    logger_name="stored_data_operation",
    file_path=os.path.join(NEW_WORK_DIR, "logs", LOG_FILE_NAME),
    level="debug",
)

my_logger = logger_instance.logger


class DataObject:
    """Define data object for future actions"""

    def __init__(self, start_time: str, end_time: str, net_adapter: str = ""):
        self.start_time = start_time
        self.end_time = end_time
        self._dt_start = datetime.fromisoformat(self.start_time)
        self._dt_end = datetime.fromisoformat(self.end_time)
        self.net_adapter = net_adapter

    def get_temp_data_frame(self) -> DataFrame:
        """Return temp data frame according requested time period"""

        data_path = os.path.abspath(os.path.join(NEW_WORK_DIR, "telemetry"))
        dir_list = os.listdir(data_path)
        # write data to temp data array
        temp_data = []

        for dir_name in dir_list:
            stored_date = datetime.strptime(dir_name, "%d-%m-%Y")
            # Find start date
            if stored_date.date() >= self._dt_start.date():

                # open csv file and converting to pandas DataFrame
                df = pd.read_csv(os.path.join(data_path, dir_name, "data.csv"))
                temp_data.append(df)
            if stored_date.date() > self._dt_end.date():
                break

        # concat all DataFrames in temp array
        result = pd.concat(temp_data)

        result["pd_time"] = pd.to_datetime(result["time"])
        start_moment = self.start_time
        end_moment = self.end_time
        return_pd = result[result["pd_time"].between(start_moment, end_moment)]
        return return_pd

    def get_net_adapter_list(self) -> list:
        """Return list of net adapters, stored in csv"""
        df = self.get_temp_data_frame()
        unique_network_list_df = pd.unique(df["network_adapter"])
        return unique_network_list_df.tolist()

    def get_network_usage_data(self, rate: float = 1) -> list:
        """Return upload and download bitrate"""
        df = self.get_temp_data_frame()
        network_df = df[["time", "network_adapter", "net_usage_up", "net_usage_down"]]
        network_df["net_usage_up"] = network_df["net_usage_up"]*rate
        network_df["net_usage_down"] = network_df["net_usage_down"]*rate
        if self.net_adapter:
            network_df = network_df[network_df["network_adapter"] == self.net_adapter]
        return network_df.values.tolist()

    def get_ram_usage(self) -> list:
        """Return ram usage data from temp DataFrame"""
        df = self.get_temp_data_frame()
        ram_df = df[["time", "ram_free"]]
        return ram_df.values.tolist()

    def get_cpu_usage(self) -> list:
        """Return cpu usage data from temp DataFrame"""
        df = self.get_temp_data_frame()
        cpu_df = df[["time", "cpu_usage"]]

        my_logger.debug("%s get_cpu_usage >>>\n %s", "DataObject class", cpu_df.head(3))

        return cpu_df.values.tolist()

    def get_csv_data(self) -> str:
        """Return all hardware usage data according requested time period"""
        data_path = os.path.abspath(os.path.join(NEW_WORK_DIR, "telemetry"))
        dir_list = os.listdir(data_path)

        # Запишем данные во временный массив
        temp_data = ""
        for dir_name in dir_list:
            stored_date = datetime.strptime(dir_name, "%d-%m-%Y")
            # Находим начальную дату
            if stored_date.date() >= self._dt_start.date():
                # Читаем csv файл
                with open(
                    os.path.join(data_path, dir_name, "data.csv"),
                    # newline='',
                    encoding="utf-8",
                ) as csvfile:
                    data_reader = csv.reader(
                        csvfile,
                        delimiter=",",
                        lineterminator="\r",
                    )
                    next(data_reader, None)  # Skip headers

                    # write data to temp array
                    for row in data_reader:
                        if (
                            datetime.fromisoformat(row[0]).time()
                            >= self._dt_start.time()
                        ):
                            temp_data += (
                                str(row).replace("[", "").replace("]", "") + "\n"
                            )
                            temp_data = temp_data.replace(" ", "")
                        if (
                            datetime.fromisoformat(row[0]).astimezone()
                            >= self._dt_end.astimezone()
                        ):
                            break

            if stored_date.date() > self._dt_end.date():
                break

        return temp_data

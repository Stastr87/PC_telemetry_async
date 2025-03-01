"""Define functions of storing data"""

import csv
import os
import sys
import time
from datetime import datetime

from async_hardware_monitor import HardWareMonitor
from env.default_env import NEW_WORK_DIR
from utils.custom_logger import CustomLogger

sys.path.append(NEW_WORK_DIR)
LOG_FILE_NAME = "data_operation.log"
logger_instance = CustomLogger(
    logger_name="data_operation",
    file_path=os.path.join(NEW_WORK_DIR, "logs", LOG_FILE_NAME),
    level="debug",
)
my_logger = logger_instance.logger


def init_collect_hw_data():
    """Saves a CSV file with data on PC resource consumption

    This code runs for 5 seconds, unless another value is passed to the HardWare Monitor() class
    Parameter monitor_period=5"""
    data = HardWareMonitor().to_dict()
    create_telemetry_data()
    update_telemetry_data_v2(data)


def init_collect_hw_data_for_display():
    """Saves a CSV file with data on PC resource consumption

    This code runs for 5 seconds, unless another value is passed to the HardWare Monitor() class
    Parameter monitor_period=5"""
    try:
        data = HardWareMonitor().to_dict()
        create_telemetry_data()
        update_telemetry_data_v2(data)
        return data
    except OSError as err:
        return f"CSV update error: {err}"


def create_telemetry_data(data_file="data.csv"):
    """Create empty csv file"""
    folder_name = os.path.abspath(
        os.path.join("telemetry", datetime.now().strftime("%d-%m-%Y"))
    )
    file_path = os.path.join(folder_name, data_file)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # Таймер для того что бы создалась директория
        time.sleep(0.2)
        with open(file_path, mode="w", encoding="utf-8") as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow(
                [
                    "time",
                    "cpu_usage",
                    "ram_free",
                    "network_adapter",
                    "net_usage_up",
                    "net_usage_down",
                ]
            )


def update_telemetry_data_v2(data: dict, file_name: str = "data.csv"):
    """Add data to *.csv file

    arguments:
    data - hardware usage data
    file_name - *.csv file name
    """
    folder_name = os.path.abspath(
        os.path.join("telemetry", datetime.now().strftime("%d-%m-%Y"))
    )
    file_path = os.path.join(folder_name, file_name)

    if not os.path.exists(file_path):
        with open(file_path, mode="w", encoding="utf-8") as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow(
                [
                    "time",
                    "cpu_usage",
                    "ram_free",
                    "network_adapter",
                    "net_usage_up",
                    "net_usage_down",
                ]
            )

    with open(file_path, mode="a", encoding="utf-8") as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        for net_adaptor in list(data["network_usage"].keys()):
            file_writer.writerow(
                [
                    datetime.now().astimezone().isoformat(),
                    round(float(data["cpu_usage"])),
                    round(float(data["ram_free"])),
                    net_adaptor,
                    round(float(data["network_usage"][net_adaptor]["up"])),
                    round(float(data["network_usage"][net_adaptor]["down"])),
                ]
            )
            # my_logger.debug("%s updated...", file_path)

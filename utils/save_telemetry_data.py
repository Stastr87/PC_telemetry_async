"""Collect telemetry data"""

import os
from sys import path

import data_operation
from utils.common_utils import TestThread
from utils.key_input import key_for_exit

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
path.append(NEW_WORK_DIR)


def collect_data():
    """Collect hardware usage data"""
    while True:
        data = data_operation.init_collect_hw_data_for_display()
        print(data)


if __name__ == "__main__":

    quit_thread = TestThread("key_for_exit", key_for_exit)
    quit_thread.start()

    collect_data_thread = TestThread("collect_data", collect_data, daemon=True)
    collect_data_thread.start()

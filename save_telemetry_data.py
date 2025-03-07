"""Collect telemetry data"""

import threading

import data_operation
from utils.key_input import key_for_exit


def collect_data():
    """Collect hardware usage data"""
    print("collect_data started")
    while True:
        data = data_operation.init_collect_hw_data_for_display()
        print(data)


if __name__ == "__main__":

    q = threading.Thread(target=key_for_exit)
    q.start()

    cd = threading.Thread(target=collect_data)
    cd.daemon = True
    cd.start()

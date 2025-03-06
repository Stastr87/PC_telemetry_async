"""Collect telemetry data"""

import threading
import time

import keyboard

import data_operation


def collect_data():
    """Collect hardware usage data"""
    print("collect_data started")
    while True:
        data = data_operation.init_collect_hw_data_for_display()
        print(data)


def wait_key():
    """Wait key process"""
    while True:
        print("Press q for exit")  # making a loop
        if keyboard.is_pressed("q"):  # if key 'q' is pressed
            print("Exit program!")
            break  # finishing the loop
        time.sleep(1)


if __name__ == "__main__":

    q = threading.Thread(target=wait_key)
    q.start()

    cd = threading.Thread(target=collect_data)
    cd.daemon = True
    cd.start()

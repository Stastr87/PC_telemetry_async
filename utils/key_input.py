"""Util for handle keyboard signals"""

import time

import keyboard


def key_for_exit():
    """Wait key process"""
    print("Press esc for exit")
    while True:
        if keyboard.is_pressed("esc"):  # if key 'q' is pressed
            print("Exit program!")
            break  # finishing the loop
        time.sleep(1)

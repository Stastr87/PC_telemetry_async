"""Util for handle keyboard signals"""

import time

import keyboard


def key_for_exit():
    """Wait key process"""
    while True:
        if keyboard.is_pressed("esc"):
            print("Exit program!")
            break
        time.sleep(1)

from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener

import time
import threading

mouse = Controller()
left_click = False
right_click = False

def left_click_loop():
    while True:
        if left_click:
            mouse.click(Button.left, 1)
            time.sleep(1)  # Click at specified interval


def right_click_loop():
    while True:
        if right_click:
            mouse.click(Button.right, 1)
            time.sleep(1)  # Click at specified interval


def on_press(key):
    global left_click
    global right_click
    if key == Key.f1:  # Start clicking or stop clicking
        right_click = False
        left_click = not left_click
    if key == Key.f2:  # Start clicking or stop clicking
        left_click = False
        right_click = not right_click


# Start the click loop in a separate thread
threading.Thread(target=left_click_loop).start()
threading.Thread(target=right_click_loop).start()

# Start the listener
with Listener(on_press=on_press) as listener:
    listener.join()

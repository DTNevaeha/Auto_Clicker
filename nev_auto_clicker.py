import tkinter as tk
from pynput.mouse import Button, Controller
import time
import threading

class AutoClicker:
    def __init__(self):
        self.mouse = Controller()
        self.clicking = False
        self.interval = 1.0
        self.counter = 0
        self.click_thread = None
        self.is_left_click = True
    
    def toggle_button(self):
        self.is_left_click = not self.is_left_click

    def toggle_clicking(self):
        if self.clicking:
            self.clicking = False
            if self.click_thread is not None:
                self.click_thread.join() # wait for the existing thread to finish
                self.click_thread = None
        else:
            self.clicking = True
            threading.Thread(target=self.click_loop).start()

    def click_loop(self):
        time.sleep(1) # delay before clicking starts
        while self.clicking:
            button = Button.left if self.is_left_click else Button.right
            self.mouse.click(button, 1)
            time.sleep(self.interval)

    def set_interval(self, interval):
        self.interval = float(interval)
    
    def stop_clicking(self):
        self.clicking = False

class AutoClickerGUI:
    def __init__(self, root, clicker):
        self.clicker = clicker

        self.button_label = tk.Label(root, text=f"Current Click: {'Left' if self.clicker.is_left_click else 'Right'}")
        self.button_label.pack()

        self.toggle_button = tk.Button(root, text="Start Clicking", command=self.toggle_clicking)
        self.toggle_button.pack()

        self.click_button = tk.Button(root, text="Toggle to Right Click", command=self.toggle_click_button)
        self.click_button.pack(pady=20)
        
        self.interval_label = tk.Label(root, text=f"Current Click Interval: {self.clicker.interval} seconds")
        self.interval_label.pack()
        self.interval_label_2 = tk.Label(root, text=f"Enter New Speed Below")
        self.interval_label_2.pack()
        self.interval_entry = tk.Entry(root)
        self.interval_entry.pack()
        self.interval_button = tk.Button(root, text="Set Click Interval", command=self.set_interval)
        self.interval_button.pack()
        
        self.button_click_count = 0

        self.counter_display = tk.Label(root, text=f"Test Click Speed Below")
        self.counter_display.pack()
        self.counter_button = tk.Button(root, text="Increase Counter", command=self.increase_counter)
        self.counter_button.pack()
        self.counter_label = tk.Label(root, text=f"Counter: {self.clicker.counter}")
        self.counter_label.pack()

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_clicking(self):
        if self.clicker.clicking:
            self.toggle_button.config(text="Start Clicking")
        else:
            self.toggle_button.config(text="Stop Clicking")
        self.clicker.toggle_clicking()

    def increase_counter(self):
        self.button_click_count += 1
        self.counter_label.config(text=f"Counter: {self.button_click_count}")

    def set_interval(self):
        try:
            interval = self.interval_entry.get()
            self.clicker.set_interval(interval)
            self.interval_label.config(text=f"Current Click Interval: {self.clicker.interval} seconds")
        except ValueError:
            pass
    
    def toggle_click_button(self):
        self.clicker.toggle_button()
        self.button_label.config(text=f"Current Click: {'Left' if self.clicker.is_left_click else 'Right'}")
        self.click_button.config(text=f"Toggle to {'Right' if self.clicker.is_left_click else 'Left'} Click")

    def on_close(self):
        self.clicker.stop_clicking()
        root.destroy()

root = tk.Tk()
root.geometry("300x400")  # Set the default size of the window to 500x500 pixels
clicker = AutoClicker()
gui = AutoClickerGUI(root, clicker)
root.mainloop()

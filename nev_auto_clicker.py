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
        frame = tk.Frame(root)
        frame.pack()

        self.button_label = tk.Label(frame, text=f"Current Click: {'Left' if self.clicker.is_left_click else 'Right'}")
        self.button_label.grid(row=0, column=0, pady=(10,0))

        self.toggle_button = tk.Button(frame, text="Start Clicking", command=self.toggle_clicking)
        self.toggle_button.grid(row=0, column=1, pady=(10,0))

        self.click_button = tk.Button(frame, text="Toggle to Right Click", command=self.toggle_click_button)
        self.click_button.grid(row=1, column=1, pady=(10,20))
        
        self.interval_label = tk.Label(frame, text=f"Click Interval: {self.clicker.interval} seconds")
        self.interval_label.grid(row=2)
        self.interval_label_2 = tk.Label(frame, text=f"Enter New Speed Below")
        self.interval_label_2.grid(row=3)
        self.interval_entry = tk.Entry(frame)
        self.interval_entry.grid(row=4, column=0)
        self.interval_button = tk.Button(frame, text="Set Click Interval", command=self.set_interval)
        self.interval_button.grid(row=4, column=1)
        
        self.counter_display = tk.Label(frame, text=f"Test Click Speed Below")
        self.counter_display.grid(row=5, column=0, pady=(20,0))
        self.button_click_count = 0
        self.counter_label = tk.Label(frame, text=f"Counter: {self.clicker.counter}")
        self.counter_label.grid(row=6, column=0)
        self.counter_button = tk.Button(frame, text="Increase Counter", command=self.increase_counter)
        self.counter_button.grid(row=6, column=1)

        self.hotkey_label = tk.Label(frame, text=f"Change Keybind to Start Clicking")
        self.hotkey_label.grid(row=7, pady=(20,0))
        self.hotkey_entry = tk.Entry(frame)
        self.hotkey_entry.grid(row=8, column=0)
        self.hotkey_entry.insert(0, '<F1>')  # Default hotkey
        self.update_hotkey_button = tk.Button(frame, text="Update Hotkey", command=self.update_hotkey)
        self.update_hotkey_button.grid(row=8, column=1)

        self.hotkey_label_2 = tk.Label(frame, text=f"Change Keybind to Toggle Left/Right")
        self.hotkey_label_2.grid(row=9, pady=(20,0))
        self.hotkey_entry_2 = tk.Entry(frame)
        self.hotkey_entry_2.grid(row=10, column=0)
        self.hotkey_entry_2.insert(0, '<F2>')  # Default hotkey
        self.update_hotkey_button_2 = tk.Button(frame, text="Update Hotkey", command=self.update_hotkey_2)
        self.update_hotkey_button_2.grid(row=10, column=1)

        self.current_hotkey = self.hotkey_entry.get()
        self.current_hotkey_2 = self.hotkey_entry_2.get()
        root.bind(self.current_hotkey, self.on_hotkey_press)  # Bind click to on_hotkey_press
        root.bind(self.current_hotkey_2, self.on_hotkey_press_2)  # Bind toggle_click to on_hotkey_press_2

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.title("Nev's Auto Clicker")
        

    def toggle_clicking(self):
        if self.clicker.clicking:
            self.toggle_button.config(text="Start Clicking")
        else:
            self.toggle_button.config(text="Stop Clicking")
        self.clicker.toggle_clicking()
    
    def update_hotkey(self):
        root.unbind(self.current_hotkey)  # Unbind the old hotkey
        self.current_hotkey = self.hotkey_entry.get()
        root.bind(self.current_hotkey, self.on_hotkey_press)  # Bind the new hotkey

    def update_hotkey_2(self):
        root.unbind(self.current_hotkey_2)  # Unbind the old hotkey
        self.current_hotkey_2 = self.hotkey_entry_2.get()
        root.bind(self.current_hotkey_2, self.on_hotkey_press_2)  # Bind the new hotkey

    def on_hotkey_press(self, event):
        self.toggle_clicking()
    
    def on_hotkey_press_2(self, event):
        self.toggle_click_button()

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
root.geometry("400x400")  # Set the default size of the window to 500x500 pixels
clicker = AutoClicker()
gui = AutoClickerGUI(root, clicker)
root.mainloop()

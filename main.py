import tkinter as tk
from tkinter import messagebox
import subprocess
import signal
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start"
        self.start_button["command"] = self.start
        self.start_button.pack(side="left")

        self.stop_button = tk.Button(self)
        self.stop_button["text"] = "Stop"
        self.stop_button["command"] = self.stop
        self.stop_button.pack(side="left")

    def start(self):
        print("Start Button Pressed")

        subprocess.Popen("./activate-school-bot.sh", shell=True)

    def stop(self):
        print("Stop Button Pressed")
        # ...
        with open('pids.txt', 'r') as file:
            lines = file.readlines()

        pid1 = int(lines[0].strip())
        pid2 = int(lines[1].strip())

        os.kill(pid1, signal.SIGTERM)
        print(f'PID1: {pid1} Killed')
        os.kill(pid2, signal.SIGTERM)
        print(f'PID2: {pid2} Killed')

root = tk.Tk()
app = Application(master=root)
app.mainloop()

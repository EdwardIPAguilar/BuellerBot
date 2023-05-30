import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import subprocess
import signal
import os
import config
import requests


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Student Replacer")  # set window title
        self.master.geometry("600x500")  # set window size
        self.configure(bg='white')  # set background color
        self.pack(fill='both', expand=True)
        self.create_widgets()

        brain_given_path = '/brain_given.txt'
        if not os.path.exists(brain_given_path):
            with open('brain_given.txt', 'w') as xr:
                xr.write("Awaiting Activation Keyword...")

        transcript_path = 'transcriptions/transcript.txt'
        if os.path.exists(transcript_path) and os.path.getsize(transcript_path) > 0:
            with open(transcript_path, 'r+') as transcript_file:
                print('wiping prior transcript')
                transcript_file.truncate()
            
        self.update_text()  

    def create_widgets(self):
        self.configure(bg='black')

        self.label = tk.Label(self, text="Student Replacer V1", bg="black", fg="white", font=('Helvetica', 24))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=3, pady=5)

        style = ttk.Style()
        style.configure('TButton', foreground='white')

        self.label = tk.Label(self, text="Live Transcript 📜", bg="black", fg="white", font=('Helvetica', 18))
        self.label.grid(row=2, column=0, pady=15)

        custom_font = font.Font(family='Helvetica', size=14)
        self.transcript_text = tk.Text(self, font=custom_font, padx=10, pady=10)
        self.transcript_text.grid(row=3, column=0, padx=15, pady=10, sticky='nsew')

        self.label2 = tk.Label(self, text="Robot Response 🤖", bg="black", fg="white", font=('Helvetica', 18))
        self.label2.grid(row=2, column=1, pady=15)

        self.brain_given_text = tk.Text(self, font=custom_font, padx=10, pady=10)
        self.brain_given_text.grid(row=3, column=1, padx=15, pady=10, sticky='nsew')

        # Add scrollbars to text widgets
        style = ttk.Style()
        style.layout('TScrollbar', [])  # Empty layout (nothing will be drawn)
        style.configure('TScrollbar', troughcolor='systemTransparent', background='systemTransparent')  # Make Scrollbar and trough transparent

        self.transcript_scrollbar = ttk.Scrollbar(self.transcript_text, orient="vertical", command=self.transcript_text.yview, style='TScrollbar')
        self.transcript_scrollbar.pack(side="right", fill="y")
        self.transcript_text.configure(yscrollcommand=self.transcript_scrollbar.set)

        self.brain_given_scrollbar = ttk.Scrollbar(self.brain_given_text, orient="vertical", command=self.brain_given_text.yview, style='TScrollbar')
        self.brain_given_scrollbar.pack(side="right", fill="y")
        self.brain_given_text.configure(yscrollcommand=self.brain_given_scrollbar.set)

        style.map('TButton', background=[('active', 'white')])
        self.upload_button = ttk.Button(self.button_frame, text="⬆️ Upload Voice", command=self.upload, style='TButton')
        self.upload_button.pack(side="left", padx=5)

        style.map('TButton', background=[('active', 'green')])
        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start, style='TButton')
        self.start_button.pack(side="left", padx=5)

        style.map('TButton', background=[('active', 'red')])
        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop, style='TButton')
        self.stop_button.pack(side="left", padx=5)

        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 1], weight=1)

    def upload(self):
        self.filename = filedialog.askopenfilename()
        messagebox.showinfo("Information", "File uploaded, processing now!")
        print(f'the path to the file is {self.filename}')
        
        print("Attempting Voice Clone")
        url = "https://api.elevenlabs.io/v1/voices/add"

        headers = {
            "Accept": "application/json",
            "xi-api-key": "a46efd8288ce2402804c3ce385d3e6b4"
        }

        data = {
            'name': 'USER_GEN',
            'labels': '{"accent": "American"}'
        }

        files = [
            ('files', (os.path.basename(self.filename), open(self.filename, 'rb'), 'audio/mpeg')),
        ]
        response = requests.post(url, headers=headers, data=data, files=files)
        custom_voice_id = response.text
        print("this is your custom voice id:", custom_voice_id)
        os.environ["AUDIO_GENERATION_ID"] = 'YepOqmv3Box1TU5q38ex'
        messagebox.showinfo("Information", "Your custom voice is ready!")

    def start(self):
        print("Start Button Pressed")
        subprocess.Popen("./activate-school-bot.sh", shell=True)

    def stop(self):
        print("Stop Button Pressed")
        with open('pids.txt', 'r') as file:
            lines = file.readlines()

        pid1 = int(lines[0].strip())
        pid2 = int(lines[1].strip())

        os.kill(pid1, signal.SIGTERM)
        print(f'PID1: {pid1} Killed')
        os.kill(pid2, signal.SIGTERM)
        print(f'PID2: {pid2} Killed')


    def update_text(self):
        transcript_path = 'transcriptions/transcript.txt'
        if os.path.exists(transcript_path) and os.path.getsize(transcript_path) > 0:
            with open(transcript_path, 'r') as transcript_file:
                transcript = transcript_file.read()

            self.transcript_text.delete('1.0', tk.END)
            self.transcript_text.insert(tk.END, transcript)
            self.transcript_text.see(tk.END)  

        brain_given_path = 'brain_given.txt'
        if os.path.exists(brain_given_path) and os.path.getsize(brain_given_path) > 0:
            with open(brain_given_path, 'r') as brain_given_file:
                brain_given = brain_given_file.read()

            self.brain_given_text.delete('1.0', tk.END)
            self.brain_given_text.insert(tk.END, brain_given)
            self.brain_given_text.see(tk.END)  

        self.after(1000, self.update_text)


root = tk.Tk()
app = Application(master=root)
app.mainloop()

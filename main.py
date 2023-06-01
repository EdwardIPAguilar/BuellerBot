import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import subprocess
import signal
import os
import config
import threading
import requests
from transcriber import start_transcription, trigger_robot
import queue
import multiprocessing

is_terminate = multiprocessing.Value('b', False)

status_queue = queue.Queue()

class TransparentScrollbar(ttk.Scrollbar):
    def set(self, *args, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def place(self, **kwargs):
        pass

    def grid(self, **kwargs):
        pass

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("🪄 BuellerBot")  # set window title
        self.master.geometry("600x500")  # set window size
        self.configure(bg='white')  # set background color
        self.pack(fill='both', expand=True)
        self.create_widgets()

        brain_given_path = '/brain_given.txt'
        if not os.path.exists(brain_given_path):
            with open('brain_given.txt', 'w') as xr:
                xr.write("Listening for activation word...")

        transcript_path = 'transcriptions/transcript.txt'
        if os.path.exists(transcript_path) and os.path.getsize(transcript_path) > 0:
            with open(transcript_path, 'w') as xr:
                xr.write("Click 'Start' to begin transcribing")
        else:
            with open(transcript_path, 'w') as xr:
                xr.write("Click 'Start' to begin transcribing")
            
        self.update_text()
        self.update_status()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.configure(bg='#323232')

        self.label = tk.Label(self, text="⚙️ BuellerBot V1", bg="#323232", fg="white", font=('Helvetica', 24))
        self.label.grid(row=0, column=0, columnspan=4, pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=4, pady=5)

        style = ttk.Style()
        style.configure('TButton', focuscolor="black")

        self.label = tk.Label(self, text="Live Transcript 📜", bg="#323232", fg="white", font=('Helvetica', 18))
        self.label.grid(row=2, column=0, pady=15)

        custom_font = font.Font(family='Helvetica', size=14)
        self.transcript_text = tk.Text(self, font=custom_font, padx=10, pady=10)
        self.transcript_text.grid(row=3, column=0, padx=15, pady=5, sticky='nsew')

        self.label2 = tk.Label(self, text="Robot Response 🤖", bg="#323232", fg="white", font=('Helvetica', 18))
        self.label2.grid(row=2, column=1, pady=15)

        frame_4th_row = tk.Frame(self, bg="#323232")
        frame_4th_row.grid(row=4, column=0, columnspan=4, pady=15, sticky='ew')

        self.hearme_label = tk.Label(frame_4th_row, text="Can you hear me now:", bg="#323232", fg="white", font=('Helvetica', 14))
        self.hearme_label.grid(row=0, column=0, padx=(10, 0), sticky='w')
        
        self.hearme_toggle_var = tk.BooleanVar(value=True)
        self.hearme_toggle = tk.Checkbutton(frame_4th_row, bg="#323232", variable=self.hearme_toggle_var)
        self.hearme_toggle.grid(row=0, column=1, sticky='w')

        self.automute_label = tk.Label(frame_4th_row, text="Auto Mute / Unmute:", bg="#323232", fg="white", font=('Helvetica', 14))
        self.automute_label.grid(row=0, column=2, padx=(10, 0), sticky='w')

        self.automute_toggle_var = tk.BooleanVar(value=True)
        self.automute_toggle = tk.Checkbutton(frame_4th_row, bg="#323232",variable=self.automute_toggle_var)
        self.automute_toggle.grid(row=0, column=3, sticky='w')

        self.status_label = tk.Label(frame_4th_row, text="Status: BuellerBot is on standby", bg="#323232", fg="white", font=('Helvetica', 14, 'italic'))
        self.status_label.grid(row=0, column=4, padx=(10, 0), sticky='w')

        self.brain_given_text = tk.Text(self, font=custom_font, padx=10, pady=10)
        self.brain_given_text.grid(row=3, column=1, padx=15, pady=5, sticky='nsew')

        style = ttk.Style()
        style.layout('TScrollbar', [])  # Empty layout (nothing will be drawn)
        style.configure('TScrollbar', troughcolor='systemTransparent', background='systemTransparent', width=0)  # Make Scrollbar and trough transparent

        self.transcript_scrollbar = TransparentScrollbar(self.transcript_text, orient="vertical", command=self.transcript_text.yview)
        self.transcript_scrollbar.pack(side="right", fill="y")
        self.transcript_text.configure(yscrollcommand=self.transcript_scrollbar.set)

        self.brain_given_scrollbar = TransparentScrollbar(self.brain_given_text, orient="vertical", command=self.brain_given_text.yview)
        self.brain_given_scrollbar.pack(side="right", fill="y")
        self.brain_given_text.configure(yscrollcommand=self.brain_given_scrollbar.set)

        self.upload_button = ttk.Button(self.button_frame, text="⬆️ Upload Voice", command=self.upload)
        self.upload_button.pack(side="left", padx=5)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=5)

        self.generate_button = ttk.Button(self.button_frame, text="⚡️ Generate Now", command=self.generate_now)
        self.generate_button.pack(side="left", padx=5)

        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 1], weight=1)

    def store_buying_time(self):
        CHUNK_SIZE = 1024
        # audio_generation_id = os.getenv("AUDIO_GENERATION_ID")
        audio_generation_id = 'lF5jGWAmp19kVdW7vg8C'
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + audio_generation_id

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": "9e72e6bd272f933f1daa508f8fe9fbc7"
        }

        params = {
            'optimize_streaming_latency': '3'
        }

        data = {
            "text": 'Hey sorry i''m having some audio issues. Is my mic working? Can you hear me?',
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)
        print(response)
        with open('buyingtime.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

    def upload(self):
        self.filenames = filedialog.askopenfilenames()
        messagebox.showinfo("Information", "Files uploaded, processing now!")
        print(f'the path to the files is {self.filenames}')
        
        print("Attempting Voice Clone")
        url = "https://api.elevenlabs.io/v1/voices/add"

        headers = {
            "Accept": "application/json",
            "xi-api-key": "9e72e6bd272f933f1daa508f8fe9fbc7"
        }

        data = {
            'name': 'USER_GEN',
            'labels': '{"accent": "American"}'
        }

        files = []
        for file in self.filenames:
            files.append(('files', (os.path.basename(file), open(file, 'rb'), 'audio/mpeg')))

        response = requests.post(url, headers=headers, data=data, files=files)
        custom_voice_id = response.text
        print("this is your custom voice id:", custom_voice_id)
        os.environ["AUDIO_GENERATION_ID"] = 'lF5jGWAmp19kVdW7vg8C'
        messagebox.showinfo("Information", "Your custom voice is ready!")
        self.store_buying_time()
    
    def generate_now(self):
        transcript_path = 'transcriptions/transcript.txt'
        if os.path.exists(transcript_path) and os.path.getsize(transcript_path) > 0:
            with open(transcript_path, 'r') as transcript_file:
                transcript = transcript_file.read()
            trigger_robot(transcript, status_queue, is_terminate)

    def start(self):
        global is_terminate
        is_terminate.value = False
        print("Start Button Pressed")
        subprocess.Popen("./activate-school-bot.sh", shell=True)
        thread = threading.Thread(target=start_transcription, args=(status_queue, is_terminate))
        thread.start()
        
    def clear_transcript(self):
        with open(config.TRANSCRIPT_FILE, 'r+') as f:
            f.truncate()
        with open("transcriptions/transcript.txt", "r+") as fx:
            fx.truncate()
        print("Transcript Cleared")

    def stop(self):
        global is_terminate
        is_terminate.value = True
        self.clear_transcript()
        print("Stop Button Pressed")
        with open('pids.txt', 'r') as file:
            lines = file.readlines()

        pid1 = int(lines[0].strip())
        pid2 = int(lines[1].strip())

        try:
            os.kill(pid1, signal.SIGTERM)
            print(f'PID1: {pid1} Killed')
        except ProcessLookupError:
            print(f"PID1: {pid1} does not exist or has already been terminated")
            
        try:
            os.kill(pid2, signal.SIGTERM)
            print(f'PID2: {pid2} Killed')
        except ProcessLookupError:
            print(f"PID2: {pid2} does not exist or has already been terminated")

    def on_closing(self):
        self.stop()
        self.master.destroy()

    def update_status(self):
        while not status_queue.empty():
            status = status_queue.get()
            self.status_label['text'] = f"Status: {status}"
        self.after(1000, self.update_status)

    def update_text(self):
        transcript_path = 'transcriptions/transcript.txt'
        if os.path.exists(transcript_path) and os.path.getsize(transcript_path) > 0:
            with open(transcript_path, 'r') as transcript_file:
                transcript = transcript_file.read().strip()

            self.transcript_text.delete('1.0', tk.END)
            self.transcript_text.insert(tk.END, transcript)
            self.transcript_text.see(tk.END)  

        brain_given_path = 'brain_given.txt'
        if os.path.exists(brain_given_path) and os.path.getsize(brain_given_path) > 0:
            with open(brain_given_path, 'r') as brain_given_file:
                brain_given = brain_given_file.read().strip()

            self.brain_given_text.delete('1.0', tk.END)
            self.brain_given_text.insert(tk.END, brain_given)
            self.brain_given_text.see(tk.END)  

        self.after(1000, self.update_text)


root = tk.Tk()
app = Application(master=root)
app.mainloop()

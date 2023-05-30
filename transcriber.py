# Suppressing annoying "NumbaDeprecationWarning"
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

import config
import whisper
import os, glob
from playsound import playsound
import openai
from textToAudio import t2a
import pyautogui as pag
import pyscreeze as ps
import ssl
import urllib.request
import asyncio
from aiofile import async_open
from typing import Tuple

# Create an unverified HTTPS context
ssl._create_default_https_context = ssl._create_unverified_context

openai.api_key = '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'

def duplicate_file(original_file_name, duplicate_file_name):
    # Open the original file in read mode
    with open(original_file_name, 'r') as original_file:
        content = original_file.read()

    # Open the duplicate file in write mode
    with open(duplicate_file_name, 'w') as duplicate_file:
        duplicate_file.write(content)

    print(f"{duplicate_file_name} has been created successfully.")

# find most recent files in a directory
recordings_dir = os.path.join('recordings', '*')

model = whisper.load_model("small")

# list to store which wav files have been transcribed
transcribed = []
print("Started Transcription")

with open(config.TRANSCRIPT_FILE, 'r+') as f:
    f.truncate()

files = glob.iglob(recordings_dir)
for x in files:
    print("deleting:", x)
    os.remove(x)

while True:
    # get most recent wav recording in the recordings directory
    files = sorted(glob.iglob(recordings_dir), key=os.path.getctime, reverse=True)
    if len(files) < 1:
        continue

    latest_recording = files[0]
    latest_recording_filename = latest_recording.split('/')[1]

    if os.path.exists(latest_recording) and not latest_recording in transcribed:
        audio = whisper.load_audio(latest_recording)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(language= 'en', fp16=False)

        result = whisper.decode(model, mel, options)

        if result.no_speech_prob < 0.5:
            print("Live Transcript: " + result.text)

            # append text to transcript file
            with open(config.TRANSCRIPT_FILE, 'a+') as f:
                f.write(result.text)
                f.truncate()
                f.seek(0)  # move file pointer to beginning
                longer_daddy = f.read()
                if len(longer_daddy) > 5000:
                    print(">>" + longer_daddy)
                    f.seek(0)
                    f.truncate()
                    f.write(longer_daddy[-5000:])

            with open("transcriptions/transcript.txt", "r") as fx:
                brain_needed = fx.read()
                if 'blueberry' in brain_needed:
                    print(f'WHAT WANT TO GIVE ROBOT: {brain_needed}')
                    print("------yepcock---------")

                    #Send to GPT for processing
                    completion = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=brain_needed,
                        max_tokens=75,
                        temperature=0
                    )
                    #save output as a variable for EL
                    brain_given = completion.choices[0].text
                    with open('brain_given.txt', 'w') as file:
                        file.write(brain_given)
                    print(f'WHAT ROBOT RESPONSED TO: {brain_needed}')
                    print(f'ROBOT ABOUT TO SAY: {brain_given}')
                    print("ROBOT IS ABOUT TO UNMUTE")
                    #Looks for muted button, then unmutes it
                    x,y = ps.locateCenterOnScreen('unmute_image.png', confidence=0.7)
                    pag.moveTo(x, y, duration=1)
                    pag.click()
                    t2a("Hello? Is my mic working? Can you hear me?")
                    playsound('output.mp3')
                    with open("transcriptions/transcript.txt", "r+") as fx:
                        fx.truncate()
                        print("Transcript Cleared")
                        # text to audio via EL
                        print("Text sent to EL API")
                        t2a(brain_given)
                        print("EL API Response Received")
                        #pass brain_given to EL code here!
                        playsound('output.mp3')
                        print("ROBOT IS ABOUT TO MUTE")
                        #looks for unmuted button, then mutes it
                        x,y = ps.locateCenterOnScreen('mic_image.png', confidence=0.7)
                        pag.moveTo(x, y, duration=1)
                        pag.click()
        # save list of transcribed recordings so that we don't transcribe the same one again
        transcribed.append(latest_recording)
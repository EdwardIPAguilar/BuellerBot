# Suppressing annoying "NumbaDeprecationWarning"
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

import config
import whisper
import time
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
from pynput.mouse import Button, Controller
import cv2
import numpy as np
from threading import Thread
from dotenv import load_dotenv

#Common transcription variations of your name. Case sensitive.
keywordOne = 'edward'
keywordTwo ='Edward'
keywordThree='eward'

is_bot_speaking = False
mouse = Controller()
load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context
openai.api_key = os.getenv('OPENAI_API_KEY')

def find_image_on_screen(image_file: str):
    screen = np.array(pag.screenshot())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    template = cv2.imread(image_file, 0)  # load template image in grayscale
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2  # return the center of the matched area

def duplicate_file(original_file_name, duplicate_file_name):
    with open(original_file_name, 'r') as original_file:
        content = original_file.read()
    with open(duplicate_file_name, 'w') as duplicate_file:
        duplicate_file.write(content)
    print(f"{duplicate_file_name} has been created successfully.")

recordings_dir = os.path.join('recordings', '*')

model = whisper.load_model("small")
transcribed = []
print("Started Transcription")

with open(config.TRANSCRIPT_FILE, 'r+') as f:
    f.truncate()

files = glob.iglob(recordings_dir)

for x in files:
    print("deleting:", x)
    os.remove(x)

def trigger_robot(brain_needed, status_queue, is_terminate):
    def run():
        global is_bot_speaking
        is_bot_speaking = True
        print('is bot speaking set 2 true')
        try:
            print(f'WHAT WANT TO GIVE ROBOT: {brain_needed}')
            status_queue.put("BuellerBot is thinking")
            print("------yepcock---------")
            #the brains of the operation
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "assistant", "content": f'INSTURCTION: You are {keywordOne}, a college student who is very smart and kind of funny. Please provide a brief, professional, and kind of funny response to the following transcript. KEEP IN MIND that the transcript will likely be cut off. TRANSCRIPT: {brain_needed} INSUTRCTION: DO NOT continue where the transcript left off -- instead, form a COMPLETE SENTENCE to respond to the most recent question. RESPONSE:'}
                ],
                max_tokens=55,
                temperature=0.2
            )
            #the lobotomy of the operation
            brain_og = completion.choices[0].message.content
            brain_given = brain_og.replace('\n', '')
            with open('brain_given.txt', 'w') as file:
                file.write(brain_given.strip())
            with open('transcriptions/transcript.txt', 'a') as file:
                file.write('\n\nPAST RESPONSE: ' + brain_given.strip() + '\n\nTRANSCRIPT:') #allows for follow-up questions. 
            print(f'WHAT ROBOT RESPONSED TO: {brain_needed}')
            print(f'ROBOT ABOUT TO SAY: {brain_given}')
            if is_terminate.value:
                raise TerminateSignal
            status_queue.put("BuellerBot is unmuting")
            print("ROBOT IS ABOUT TO UNMUTE")
            #search for mute button
            x, y = find_image_on_screen('g_unmute.png')
            mouse.position = (x, y)
            mouse.click(Button.left, 1)
            time.sleep(1)
            mouse.click(Button.left, 1)
            status_queue.put("BuellerBot is buying time")
            if is_terminate.value:
                raise TerminateSignal
            t2a("Hey sorry i''m having some audio issues. Is my mic working? Can you hear me?")
            is_bot_speaking = True
            print('is bot speaking set 2 true')
            playsound('output.mp3')
            # with open("transcriptions/transcript.txt", "r+") as fx:
            #     fx.truncate()
            print("Transcript Cleared")
            print("Text sent to EL API")
            if is_terminate.value:
                raise TerminateSignal
            status_queue.put("BuellerBot is generating")
            t2a(brain_given)
            print("EL API Response Received")
            status_queue.put("BuellerBot is responding")
            is_bot_speaking = True
            print('is bot speaking set 2 true')
            playsound('output.mp3')
            time.sleep(5) #allow it to respond w/o getting caught in the transcript
            status_queue.put("BuellerBot is about to mute")
            print("ROBOT IS ABOUT TO MUTE")
            is_bot_speaking = True
            print('is bot speaking set 2 true')
            x, y = find_image_on_screen('g_mute.png')
            mouse.position = (x, y)
            mouse.click(Button.left, 1)
            status_queue.put("BuellerBot is on standby")
            is_bot_speaking = False
            print('is bot speaking set 2 false')
        finally:
            is_bot_speaking = False
            print('is bot speaking set 2 false')
            # Add some delay here to ensure the bot is fully finished before resuming transcription
    Thread(target=run).start()

class TerminateSignal(Exception):
    pass

def start_transcription(status_queue, is_terminate):
    global is_bot_speaking
    status_queue.put("BuellerBot is listening")
    
    while True:
        if is_bot_speaking:
            continue

        if is_terminate.value:
            print("terminate hit, break function")
            break
        # get most recent wav recording in the recordings directory
        try:
            files = sorted(glob.iglob(recordings_dir), key=os.path.getctime, reverse=True)
        except FileNotFoundError:
            files = []
        if len(files) < 1:
            continue
        latest_recording = files[0]
        latest_recording_filename = latest_recording.split('/')[1]
        if is_bot_speaking:
                    continue
        if os.path.exists(latest_recording) and not latest_recording in transcribed:
            audio = whisper.load_audio(latest_recording)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            options = whisper.DecodingOptions(language= 'en', fp16=False)
            result = whisper.decode(model, mel, options)
            if is_bot_speaking:
                continue
            if result.no_speech_prob < 0.5:
                if is_bot_speaking:
                    continue
                print("Live Transcript: " + result.text)
                with open(config.TRANSCRIPT_FILE, 'a+') as f:
                    if is_bot_speaking:
                        continue
                    f.write(result.text)
                    f.truncate()
                    f.seek(0)  
                    longer_daddy = f.read()
                    if len(longer_daddy) > 5000:
                        print(">>" + longer_daddy)
                        f.seek(0)
                        f.truncate()
                        f.write(longer_daddy[-5000:])

                with open("transcriptions/transcript.txt", "r") as fx:
                    brain_needed = fx.read()
                    if is_bot_speaking:
                        continue
                    if keywordOne in brain_needed or keywordTwo in brain_needed or keywordThree in brain_needed:
                        print('trigger word noted, waiting 1 second for additional context')
                        time.sleep(1.5) #keep recording for 1.5 seconds in case of additional context
                        trigger_robot(brain_needed, status_queue, is_terminate)
                        brain_needed = brain_needed.replace(keywordOne, '')
                        brain_needed = brain_needed.replace(keywordTwo, '')
                        brain_needed = brain_needed.replace(keywordThree, '')
                        with open("transcriptions/transcript.txt", "w") as fw:
                            fw.write(brain_needed)
            
            transcribed.append(latest_recording)

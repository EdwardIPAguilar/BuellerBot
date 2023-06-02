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
import ssl
import urllib.request
from threading import Thread
from dotenv import load_dotenv

#Common transcription variations of your name. Case sensitive.
keywordOne = 'edward'
keywordTwo ='Edward'
keywordThree='eward'

is_bot_speaking = False
load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context
openai.api_key = os.getenv('OPENAI_API_KEY')

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

        try:
            #bot unmutes and buys you time
            status_queue.put("BuellerBot is buying time")
            location = pag.locateOnScreen('unmute_image.png')
            if location is not None:
                x,y,width,height=location
                center_x = x + width // 2
                center_y = y + height // 2
                pag.moveTo(center_x,center_y,duration=0.5)
                pag.click(clicks=2)
            else:
                print("Bot could not find unmute image")
            is_bot_speaking = True
            Thread(target=playsound, args=('buyingtime.mp3',)).start()

            if is_terminate.value:
                raise TerminateSignal
            
            #bot generates response in the background
            status_queue.put("BuellerBot is thinking")
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "assistant", "content": f'INSTURCTION: You are {keywordOne}, a college student who is very smart and kind of funny. Please provide a brief, professional, and kind of funny response to the following transcript. KEEP IN MIND that the transcript will likely be cut off. TRANSCRIPT: {brain_needed} INSUTRCTION: DO NOT continue where the transcript left off -- instead, form a COMPLETE, BRIEF SENTENCE to respond to the most recent question. RESPONSE:'}
                ],
                max_tokens=55,
                temperature=0.2
            )
            brain_og = completion.choices[0].message.content
            brain_given = brain_og.replace('\n', '')
            with open('brain_given.txt', 'w') as file:
                file.write(brain_given.strip())
            with open('transcriptions/transcript.txt', 'a') as file:
                file.write('\n\nPAST RESPONSE: ' + brain_given.strip() + '\n\nTRANSCRIPT:') #allows for follow-up questions. 
            print(f'Bot Going To Say: {brain_given}')

            if is_terminate.value:
                raise TerminateSignal

            #bot generates voice and talks
            t2a(brain_given)
            is_bot_speaking = True
            status_queue.put("BuellerBot is responding")
            playsound('output.mp3')
            is_bot_speaking = False

            if is_terminate.value:
                raise TerminateSignal

            #bot mutes            
            status_queue.put("BuellerBot is about to mute")
            location = pag.locateOnScreen('mic_image.png')
            if location is not None:
                x,y,width,height=location
                center_x = x + width // 2
                center_y = y + height // 2
                pag.moveTo(center_x,center_y,duration=0.5)
                pag.click(clicks=2)
            else:
                pag.click(clicks=1)
                print("Bot could not find mute image, guessing that it is hidden under mouse")
            status_queue.put("BuellerBot is on standby")

        finally:
            is_bot_speaking = False
    Thread(target=run).start()

class TerminateSignal(Exception):
    pass

def start_transcription(status_queue, is_terminate):
    global is_bot_speaking
    status_queue.put("BuellerBot is listening")
    
    while True:

        if is_bot_speaking:
            print('bot speaking flagged')
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
        # get most recent wav recording in the recordings directory

        if is_bot_speaking:
            print('bot speaking flagged')
            continue
        if is_terminate.value:
            print("terminate hit, break function")
            break
    
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
                    transcript_text = f.read()
                    if len(transcript_text) > 5000:
                        print(">>" + transcript_text)
                        f.seek(0)
                        f.truncate()
                        f.write(transcript_text[-5000:])

                with open("transcriptions/transcript.txt", "r") as fx:
                    brain_needed = fx.read()
                    if is_bot_speaking:
                        print('bot speaking flagged')
                        continue
                    if is_terminate.value:
                        print("terminate hit, break function")
                        break
                    if keywordOne in brain_needed or keywordTwo in brain_needed or keywordThree in brain_needed:
                        print('trigger word noted, waiting 1 second for additional context')
                        time.sleep(1.5) #keep recording for 1.5 seconds in case of additional context
                        trigger_robot(brain_needed, status_queue, is_terminate)
                        brain_needed = brain_needed.replace(keywordOne, '') #this prevents from endless bot loop
                        brain_needed = brain_needed.replace(keywordTwo, '')
                        brain_needed = brain_needed.replace(keywordThree, '')
                        with open("transcriptions/transcript.txt", "w") as fw:
                            fw.write(brain_needed)
            
            transcribed.append(latest_recording)
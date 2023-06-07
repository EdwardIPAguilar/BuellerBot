import requests
import os
from dotenv import load_dotenv

#this file is for if you get an error saying that you've used up all your voices:
#take the most recent voice id, and pass it through the 'deleteVoices' function
#run the code and you should get a confirmation 'ok' printed out, you can now create more voices.

load_dotenv()
EL_API_KEY = os.getenv('EL_API_KEY')

def deleteVoices(voiceID):
  print("Attempting To Delete Voice")
  url = "https://api.elevenlabs.io/v1/voices/" + voiceID

  headers = {
    "Accept": "application/json",
    "xi-api-key": EL_API_KEY
  }

  response = requests.delete(url, headers=headers)
  print(response.text)

deleteVoices("default")

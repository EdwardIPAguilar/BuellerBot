import requests

def deleteVoices(voiceID):
  print("Attempting To Delete Voice")
  url = "https://api.elevenlabs.io/v1/voices/" + voiceID

  headers = {
    "Accept": "application/json",
    "xi-api-key": "9e72e6bd272f933f1daa508f8fe9fbc7"
  }

  response = requests.delete(url, headers=headers)
  print(response.text)

deleteVoices("qSRWIsp602dFWUQe56Uj")

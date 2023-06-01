import requests

def deleteVoices(voiceID):
  print("Attempting To Delete Voice")
  url = "https://api.elevenlabs.io/v1/voices/" + voiceID

  headers = {
    "Accept": "application/json",
    "xi-api-key": "a46efd8288ce2402804c3ce385d3e6b4"
  }

  response = requests.delete(url, headers=headers)
  print(response.text)

deleteVoices("mIn0JUGno1hwWyH63tCH")

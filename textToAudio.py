import requests
import os

def t2a(input_text):
    CHUNK_SIZE = 1024
    # audio_generation_id = os.getenv("AUDIO_GENERATION_ID")
    audio_generation_id = 'YepOqmv3Box1TU5q38ex'
    print("this is my current voice ID:", audio_generation_id)
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + audio_generation_id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "a46efd8288ce2402804c3ce385d3e6b4"
    }

    params = {
        'optimize_streaming_latency': '3'
    }

    data = {
        "text": input_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    print(response)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
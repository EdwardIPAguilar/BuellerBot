import requests
import os

def t2a(input_text):
    CHUNK_SIZE = 1024
    # audio_generation_id = os.getenv("AUDIO_GENERATION_ID")
    audio_generation_id = 'lF5jGWAmp19kVdW7vg8C'
    # print("this is my current voice ID:", audio_generation_id)
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
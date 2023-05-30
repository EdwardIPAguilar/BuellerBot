import sounddevice as sd
import wavio as wv
import datetime

freq = 44100
duration = 5 # in seconds
print('Started Recording')
# print(sd.query_devices())
while True:
    ts = datetime.datetime.now()
    filename = ts.strftime("%Y-%m-%d %H:%M:%S")
    device_id = 1 #you can use print(sd.query_devices()) to find the index of your device
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, device=device_id)

    # Record audio for the given number of seconds
    sd.wait()

    # Convert the NumPy array to audio file
    wv.write(f"./recordings/{filename}.wav", recording, freq, sampwidth=2)
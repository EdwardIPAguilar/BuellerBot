import sounddevice as sd
import wavio as wv
import datetime

freq = 44100
duration = 5 # in seconds

print('Started Recording')
# cock
while True:
    ts = datetime.datetime.now()
    filename = ts.strftime("%Y-%m-%d %H:%M:%S")

    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

    # Record audio for the given number of seconds
    sd.wait()

    # Convert the NumPy array to audio file
    wv.write(f"./recordings/{filename}.wav", recording, freq, sampwidth=2)
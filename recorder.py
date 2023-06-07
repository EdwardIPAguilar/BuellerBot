import sounddevice as sd
import wavio as wv
import datetime

def get_device_id_by_name(name):
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if name.lower() in device['name'].lower():
            return i
    return None

freq = 44100
duration = 5 # in seconds
print('Started Recording')

device_id = get_device_id_by_name("Blackhole 2ch") #if you download another blackhole version, update this to its name

if device_id is None:
    print('Blackhole device not found')
    exit(1)

while True:
    ts = datetime.datetime.now()
    filename = ts.strftime("%Y-%m-%d %H:%M:%S")

    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, device=device_id)

    # Record audio for the given number of seconds
    sd.wait()

    # Convert the NumPy array to audio file
    wv.write(f"./recordings/{filename}.wav", recording, freq, sampwidth=2)
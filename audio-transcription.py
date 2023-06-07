# Suppressing "NumbaDeprecationWarning"
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

# normal code poggers
import whisper
model = whisper.load_model("small")
result = model.transcribe("audio-test.mp3")
print(result["text"])
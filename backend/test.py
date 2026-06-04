from audio import record_audio
from stt import transcribe

file = record_audio(duration=5)
text = transcribe(file)

print("You said:", text)
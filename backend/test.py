from vad import record_with_vad
from audio import save_audio

audio = record_with_vad()
file = save_audio(audio)

print("Saved:", file)
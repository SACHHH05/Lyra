from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def transcribe(audio_path):
    print("Lyra is thinking (transcribing)...")

    segments, info = model.transcribe(audio_path)

    text = ""
    for segment in segments:
        text += segment.text + " "

    return text.strip()
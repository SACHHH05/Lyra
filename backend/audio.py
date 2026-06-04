import sounddevice as sd
import wave

SAMPLE_RATE = 16000
CHANNELS = 1

def record_audio(duration=5, filename="input.wav"):
    print("Lyra is listening...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16'
    )

    sd.wait()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    print(f"Saved: {filename}")
    return filename

def save_audio(audio, filename="input.wav", sample_rate=16000):
    audio = (audio * 32767).astype("int16")

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    return filename
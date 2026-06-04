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
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 16000
CHANNELS = 1

def record_audio(duration=5, filename="input.wav"):

    """
    Records audio from microphone and saves it as WAV file
    """

    print("🎤 Lyra is listening...")

    # Record audio
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16'
    )

    sd.wait()  

    write(filename, SAMPLE_RATE, audio)

    print(f"Audio saved: {filename}")

    return filename
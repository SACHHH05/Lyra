import torch
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000

model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)

(get_speech_timestamps, _, read_audio, _, _) = utils


def record_with_vad(max_duration=10):
    """
    Simple stable VAD-based recording
    """

    print("Lyra is listening (VAD mode)...")

    audio_buffer = []

    def callback(indata, frames, time, status):
        audio_buffer.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32',
        callback=callback
    ):
        sd.sleep(int(max_duration * 1000))

    audio = np.concatenate(audio_buffer, axis=0)

    wav = torch.tensor(audio.squeeze())

    speech_timestamps = get_speech_timestamps(
        wav,
        model,
        sampling_rate=SAMPLE_RATE
    )

    if not speech_timestamps:
        print("No speech detected")
        return audio

    speech_audio = []
    for ts in speech_timestamps:
        speech_audio.append(audio[ts['start']:ts['end']])

    final_audio = np.concatenate(speech_audio, axis=0)

    print("Speech extracted successfully")

    return final_audio
import torch
import numpy as np
from config import SAMPLE_RATE, VAD_THRESHOLD

class VADProcessor:
    def __init__(self):
        self.model, _ = torch.hub.load(
            'snakers4/silero-vad',
            'silero_vad',
            trust_repo=True
        )
        self.speech_buffer = []
        self.is_speaking = False

    def _predict(self, audio_chunk):
        if len(audio_chunk) < 512:
            return 0.0

        # Silero VAD expects a 2D tensor batch shape: [batch_size, time]
        audio_tensor = torch.tensor(audio_chunk, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            prob = self.model(audio_tensor, SAMPLE_RATE).item()

        return prob

    def is_speech(self, chunk):
        prob = self._predict(chunk)
        return prob > VAD_THRESHOLD

    def add_speech(self, chunk):
        self.speech_buffer.extend(chunk)
        self.is_speaking = True

    def reset(self):
        self.speech_buffer = []
        self.is_speaking = False

    def has_speech(self):
        return len(self.speech_buffer) > SAMPLE_RATE * 0.3  

    def get_audio(self):
        return np.array(self.speech_buffer, dtype=np.float32)
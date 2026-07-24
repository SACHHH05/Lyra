import numpy as np
from faster_whisper import WhisperModel

class STT:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        model_size: tiny / base / small / medium / large-v3
        device: cpu or cuda
        compute_type: int8 (fast + lightweight) OR float16 (GPU)
        """
        print("Loading Faster Whisper model...")
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
        print("STT ready.")

    def transcribe(self, audio_bytes, sample_rate=16000):
        """
        audio_bytes: raw PCM float32 or int16 audio array
        returns: clean transcript string
        """
        try:
            audio = np.array(audio_bytes, dtype=np.float32)

            if audio.max() > 1.0:
                audio = audio / 32768.0

            if len(audio) < sample_rate * 0.5:  
                return ""

            segments, info = self.model.transcribe(
                audio,
                language="en",
                beam_size=5,
                vad_filter=True  
            )

            text = "".join(segment.text for segment in segments)
            return text.strip()

        except Exception as e:
            print("STT error:", e)
            return ""

# Initialize a single shared instance of the model 
_stt_instance = STT()

# Expose the functional interface your websocket.py file is expecting
def transcribe_audio(audio_bytes):
    return _stt_instance.transcribe(audio_bytes)
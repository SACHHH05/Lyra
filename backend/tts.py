from pykokoro import KokoroPipeline, PipelineConfig

class TTS:
    def __init__(self, voice="af_sarah"):
        self.config = PipelineConfig(voice=voice)
        self.pipeline = KokoroPipeline(self.config)
        print("TTS ready.")

    def generate_audio(self, text):
        """
        Converts text to raw PCM audio bytes.
        """
        try:
            result = self.pipeline.run(text)
            
            return result.audio.tobytes()
        except Exception as e:
            print("TTS error:", e)
            return None

_tts_instance = TTS()

def synthesize_speech(text):
    return _tts_instance.generate_audio(text)
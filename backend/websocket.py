import numpy as np
from vad import VADProcessor
from stt import transcribe_audio  
from llm import LLM
from tts import synthesize_speech
from config import SAMPLE_RATE, CHUNK_SIZE

llm = LLM()
vad = VADProcessor()

async def handle_connection(websocket):
    await websocket.accept()
    print("Lyra WebSocket Connected")

    audio_buffer = []

    try:
        while True:
            data = await websocket.receive_bytes()
            chunk = np.frombuffer(data, dtype=np.float32).tolist()
            audio_buffer.extend(chunk)

            if len(audio_buffer) > SAMPLE_RATE * 10:
                audio_buffer = audio_buffer[-SAMPLE_RATE * 10:]

            if len(audio_buffer) < CHUNK_SIZE:
                continue

            window = audio_buffer[-CHUNK_SIZE:]

            if vad.is_speech(window):
                vad.add_speech(window)
            else:
                if vad.has_speech():
                    print("Speech detected, processing...")
                    full_audio = vad.get_audio()
                    vad.reset()

                    text = transcribe_audio(full_audio)
                    print("User:", text)

                    if not text:
                        continue

                    response = llm.ask(
                        prompt=text,
                        system_prompt="You are Lyra, a helpful voice AI assistant."
                    )

                    print("Lyra:", response)

                    await websocket.send_json({
                        "input": text,
                        "response": response
                    })
                    audio_bytes = synthesize_speech(response)
                    
                    if audio_bytes:
                        await websocket.send_bytes(audio_bytes)
                    
                    await websocket.send_json({
                        "input": text,
                        "response": response,
                        "status": "audio_sent"
                    })
                    
                    audio_buffer = []
    except Exception as e:
        print("WebSocket error:", e)
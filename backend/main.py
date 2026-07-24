import wave
import numpy as np
from fastapi import FastAPI, WebSocket
from websocket import handle_connection
from pydantic import BaseModel

from audio import record_audio
from stt import transcribe_audio  
from llm import LLM              

app = FastAPI()
llm_instance = LLM()             

class RequestBody(BaseModel):
    text: str

@app.websocket("/ws/audio")
async def audio_ws(websocket: WebSocket):
    await handle_connection(websocket)

@app.get("/")
def home():
    return {"message": "Lyra is alive"}

@app.post("/talk")
def talk():
    """
    Full pipeline:
    audio → stt → llm → response
    """
    # Records audio and returns a filename string (e.g. "input.wav")
    file_path = record_audio(duration=5)
    
    # Read the saved wav file frames back as a numerical array for transcription
    with wave.open(file_path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

    text = transcribe_audio(audio_data)
    reply = llm_instance.ask(text)

    return {
        "input": text,
        "response": reply
    }
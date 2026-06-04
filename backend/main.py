from fastapi import FastAPI
from pydantic import BaseModel

from audio import record_audio
from stt import transcribe
from llm import ask_llm

app = FastAPI()

class RequestBody(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Lyra is alive"}


@app.post("/talk")
def talk():
    """
    Full pipeline:
    audio → stt → llm → response
    """

    file = record_audio(duration=5)
    text = transcribe(file)
    reply = ask_llm(text)

    return {
        "input": text,
        "response": reply
    }
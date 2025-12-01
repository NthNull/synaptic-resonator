from fastapi import FastAPI, Response
from synaptic_resonator.generator import generate_waveform, generate_fragment
from pydantic import BaseModel

app = FastAPI(title="Synaptic Resonator")

class InputData(BaseModel):
    input: str

@app.post("/resonate")
async def resonate(data: InputData):
    input_text = data.input
    waveform, sr = generate_waveform(input_text)
    fragment = generate_fragment(input_text)
    # convert to bytes (float32 little-endian)
    audio_bytes = waveform.tobytes()
    headers = {"X-Memory-Fragment": fragment, "X-Sample-Rate": str(sr)}
    return Response(content=audio_bytes, media_type="application/octet-stream", headers=headers)

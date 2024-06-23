# app/main.py
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

from processing.audio_input import record_audio, transcribe_audio
from processing.model_input import get_response

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class RecordAudioRequest(BaseModel):
    filename: str
    record_seconds: int
    sample_rate: int
    chunk: int

class AudioOutput(BaseModel): 
    filename: str

class TextOutput(BaseModel):
    text: str

class MessageResponse(BaseModel):
    message: str

class TranscriptionResponse(BaseModel):
    transcription: str

class ModelResponse(BaseModel):
    response: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/record", response_model=MessageResponse)
async def record_audio_endpoint(request: RecordAudioRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(record_audio, request.filename, request.record_seconds, request.sample_rate, request.chunk)
    return MessageResponse(message="Recording started")

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    try:
        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
        file_location = os.path.join(temp_dir, file.filename)
        
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        
        transcription = transcribe_audio(file_location, client)
        os.remove(file_location)
        return TranscriptionResponse(transcription=transcription)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/get_response", response_model=ModelResponse)
async def get_response_endpoint(request: TextOutput):
    response = get_response(request.text, client)
    return ModelResponse(response=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

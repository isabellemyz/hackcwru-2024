# UNTESTED AND UNEDITED CHATGPT CODE

# app/main.py
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

from processing.audio_input import record_audio
from processing.audio_input import transcribe_audio
from processing.model_input import get_response

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

class RecordAudioRequest(BaseModel):
    filename: str
    record_seconds: int
    sample_rate: int
    chunk: int

class AudioOutput(BaseModel): 
    filename: str


class TextOutput(BaseModel):
    text: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/record")
async def record_audio_endpoint(request: RecordAudioRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(record_audio, request.filename, request.record_seconds, request.sample_rate, request.chunk)
    return JSONResponse(content={"message": "Recording started"})

@app.post("/transcribe")
async def transcribe_audio_endpoint(request: AudioOutput):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    transcription = transcribe_audio(request.filename, client)
    # os.remove("temp_audio.wav")
    return JSONResponse(content={"transcription": transcription})

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     upload_dir = "uploads/"
#     os.makedirs(upload_dir, exist_ok=True)
#     file_path = os.path.join(upload_dir, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {"filename": file.filename}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import pyaudio
import wave
from dotenv import load_dotenv
import os
from log_setup import get_logger

logger = get_logger()

def record_audio(output_filename, record_seconds=5, sample_rate=44100, chunk=1024):
    # recording logic
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    logger.debug("Recording...")

    frames = []

    for _ in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    logger.debug("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # if output file path DNE, then make it
    directory = os.path.dirname(output_filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # writing logic
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def transcribe_audio_deprecated(file_path, client):
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(model="whisper-1", 
        file=audio_file)

    return transcription.text
import pyaudio
import wave
import whisper
from openai import OpenAI
from openai import OpenAI


from dotenv import load_dotenv
import os

# loading variables from .env file
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def record_audio(output_filename, record_seconds=5, sample_rate=44100, chunk=1024):
    # recording logic
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    for _ in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

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

def transcribe_audio(file_path):

    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(model="whisper-1", 
        file=audio_file)
    return transcription.text

if __name__ == "__main__":
    audio_file = "whisper_ai/audio_data/test_audio.wav"

    # Record audio from the microphone
    record_audio(audio_file, record_seconds=5)

    # Get the transcription of the recorded audio
    transcription = transcribe_audio("whisper_ai/audio_data/test_audio.wav")

    # Print the transcription
    print("Transcription: ", transcription)

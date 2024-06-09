import pyaudio
import wave
import whisper
from openai import OpenAI
from openai import OpenAI


from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

# Now you can access the variables using os.environ
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def record_audio(output_filename, record_seconds=5, sample_rate=44100, chunk=1024):
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

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

# def transcribe_audio(file_path):
#     client = OpenAI(api_key)

#     audio_file = open(file_path, "rb")
#     transcription = client.audio.transcriptions.create(
#         model="whisper-1", 
#         file=audio_file
#     )
#     print(transcription.text)


# def transcribe_audio(file_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(file_path)
#     return result["text"]require

def transcribe_audio(file_path):

    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(model="whisper-1", 
        file=audio_file)
    return transcription.text

if __name__ == "__main__":
    audio_file = "vocally-project/WhisperAI/Audio/test_audio.wav"

    # Record audio from the microphone
    record_audio(audio_file, record_seconds=5)

    # Get the transcription of the recorded audio
    transcription = transcribe_audio("vocally-project/WhisperAI/Audio/test_audio.wav")

    # Print the transcription
    print("Transcription: ", transcription)

from openai import OpenAI
from dotenv import load_dotenv
import os

from processing.audio_input import record_audio
from processing.audio_input import transcribe_audio
from processing.model_input import get_response

if __name__ == '__main__':
    #initialize here
    # call record -> transcribe -> get_response

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    audio_file = "processing/audio_data/test_audio.wav"

    # Record audio from the microphone
    record_audio(audio_file, record_seconds=5)

    # Get the transcription of the recorded audio
    transcription = transcribe_audio("processing/audio_data/test_audio.wav", client)

    response = get_response(transcription, client)

    # Print the transcription
    print("Transcription: ", transcription)
    print("Response", response)
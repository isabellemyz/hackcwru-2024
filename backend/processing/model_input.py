import os
from processing.conversation import Conversation
from pathlib import Path

context_length = 128000

conversation = Conversation()


# Function to interact with ChatGPT
def get_response(user_input, client):
    conversation.add_message("user", user_input)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation.history,
        response_format={ "type": "json_object" } # this makes it return only one JSON key-value
    )

    conversation.add_message("assistant", response.choices[0].message.content)
    print(conversation.history)

    total_tokens = conversation.get_total_tokens()

    return response.choices[0].message.content

def get_response_audio(text, client):
    try:
        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        speech_file_path = Path(temp_dir) / "speech.mp3"

        audio_response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )

        audio_response.stream_to_file(speech_file_path)

        with open(speech_file_path, "rb") as f:
            audio_data = f.read()

        # os.remove(speech_file_path)

        print("all good")

        return audio_data
    except Exception as e:
        raise RuntimeError(f"error generating audio: {str(e)}")

def refresh_chat():
    conversation.clear()
    print(conversation.get_total_tokens())
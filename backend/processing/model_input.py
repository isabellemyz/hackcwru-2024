from openai import OpenAI
from dotenv import load_dotenv
import os
from processing.conversation import Conversation
from log_setup import get_logger

logger = get_logger()

context_length = 128000

conversation = Conversation()


# Function to interact with ChatGPT
def get_response(user_input, client):
    # Append the user input to the conversation history
    conversation.add_message("user", user_input)
    logger.debug(f"User: {user_input}")

    # Call the OpenAI API with the conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation.history,
        response_format={ "type": "json_object" } # this makes it return only one JSON key-value
    )

    conversation.add_message("assistant", response.choices[0].message.content)
    logger.debug(f"Model answer: {response.choices[0].message.content}")

    #total_tokens = conversation.get_total_tokens()
    conversation.check_token_threshold(client)
    
    return response.choices[0].message.content

def refresh_chat():
    conversation.clear()
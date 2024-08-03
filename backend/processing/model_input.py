from openai import OpenAI
from dotenv import load_dotenv
import os
from processing.conversation import Conversation

context_length = 128000

conversation = Conversation()


# Function to interact with ChatGPT
def get_response(user_input, client):
    # Append the user input to the conversation history
    conversation.add_message("user", user_input)
    
    conversation.check_token_threshold(client)

    # Call the OpenAI API with the conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation.history,
        response_format={ "type": "json_object" } # this makes it return only one JSON key-value
    )

    conversation.add_message("assistant", response.choices[0].message.content)
    print(conversation.history)

    total_tokens = conversation.get_total_tokens()
    
    
    return response.choices[0].message.content

def refresh_chat():
    conversation.clear()
    print(conversation.get_total_tokens())
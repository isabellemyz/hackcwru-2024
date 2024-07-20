from openai import OpenAI
from dotenv import load_dotenv
import os
from processing.conversation import Conversation

context_length = 128000

conversation = Conversation()


# Function to interact with ChatGPT
def get_response(user_input, client):
    # Append the user input to the conversation history
    # conversation_history.append({"role": "user", "content": user_input})
    conversation.add_message("user", user_input)
    
    # Call the OpenAI API with the conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation.history
    )
    
    # conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    conversation.add_message("assistant", response.choices[0].message.content)
    print(conversation.history)

    total_tokens = conversation.get_total_tokens()
    
    # if total_tokens > context_length:
        # summary model
    # print(total_tokens)
    
    
    return response.choices[0].message.content

def refresh_chat():
    conversation.clear()
    print(conversation.get_total_tokens())

# if __name__ == "__main__":
#     test_history = [{"role": "assistant", "content": "content 1"}, {"role": "system", "content": "content 2", "hint": "hint!!!"}]

#     num_tokens(test_history, "gpt-3.5-turbo-0125")
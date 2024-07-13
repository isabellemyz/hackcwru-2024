from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

global exceed_context_length

global conversation_history

exceed_context_length = False

conversation_history = [
    {"role": "system", "content": "You are a tech interviewer helper you must help the interviewee. Output your response in JSON"}
]

'''
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]
'''

# Function to interact with ChatGPT
def get_response(user_input, client):
    # Append the user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Call the OpenAI API with the conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=conversation_history
    )
    
    #print(response['choices'][0]['message']['content'])
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    print(conversation_history)
    return response.choices[0].message.content

def num_tokens(history, model_name) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    conversation_string = ""
    
    for dictionary in history:
        for key in dictionary.keys():
            conversation_string += dictionary[key]
    
    print('convo string', conversation_string)
    
    num_tokens = len(encoding.encode(conversation_string))

    print('num tokens', num_tokens)

    return num_tokens

# if __name__ == "__main__":
#     test_history = [{"role": "assistant", "content": "content 1"}, {"role": "system", "content": "content 2", "hint": "hint!!!"}]

#     num_tokens(test_history, "gpt-3.5-turbo-0125")
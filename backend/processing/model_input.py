from openai import OpenAI
from dotenv import load_dotenv
import os

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


# def get_response(transcription, client):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo-0125",
#         response_format={ "type": "json_object" },
#         messages=[
#             {"role": "system", "content": "You are a tech interviewer helper you must help the interviewee. Output your response in JSON"},
#             {"role": "user", "content": transcription}
#         ]
#     )

#     return response.choices[0].message.content
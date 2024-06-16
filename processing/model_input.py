from openai import OpenAI
from dotenv import load_dotenv
import os

# load_dotenv()
# api_key = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

def get_response(transcription, client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a tech interviewer helper you must help the interviewee. Output your response in JSON"},
            {"role": "user", "content": transcription}
        ]
    )

    return response.choices[0].message.content
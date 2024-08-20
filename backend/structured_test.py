
from processing.conversation import Conversation
from log_setup import get_logger
from openai import OpenAI
from dotenv import load_dotenv
import os

logger = get_logger()
import sys
logger.debug(f"Running Python version: {sys.version}")


conversation = Conversation()

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_response(user_input, client):
    conversation.add_message("user", user_input)
    logger.debug(f"User: {user_input}")
    logger.debug(conversation.history)
    # Call the OpenAI API with the conversation history
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=conversation.history,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "InterviewResponse",
                "schema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": ["object", "null"],  # Allow question to be null
                            "description": "Details of the question. If interviewee has not asked you for a question, put null.",
                            "properties": {
                                "description": {
                                    "type": ["string", "null"],
                                    "description": "The question to ask the interviewee."
                                },
                                "example": {
                                    "type": ["string", "null"],
                                    "description": "An example of the question."
                                },
                                "constraints": {
                                    "type": ["array", "null"],
                                    "description": "Constraints or conditions applied to the question.",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },
                            "required": ["description", "example", "constraints"],
                            "additionalProperties": False
                        },
                        "final_response": {
                            "type": "string",
                            "description": "The final response given to the interviewee."
                        },
                    },
                    "required": ["final_response", "question"], 
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    logger.debug(response)
    return response.choices[0].message.parsed


if __name__ == "__main__":
    user_input = "Can you ask me a question about dynamic programming?"

    response_json = get_response(user_input, client)

    
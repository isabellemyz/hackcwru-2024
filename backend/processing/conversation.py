import tiktoken
from log_setup import get_logger

logger = get_logger()

# Initialize encoder
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

class Conversation:
    def __init__(self):
        self.history = [
            {"role": "system", "content": "You are a tech interviewer helper you must help the interviewee. Output your response in JSON"}
        ]
        self.total_tokens = 0
        self.token_threshold = 300

    def add_message(self, role, message):
        self.history.append({"role": role, "content": message})
        self.total_tokens += len(enc.encode(message))
    
    def clear(self):
        self.history.clear()
        self.history.append({"role": "system", "content": "You are a tech interviewer helper you must help the interviewee. Output your response in JSON"})
        self.total_tokens = len(enc.encode(self.history[0]["content"]))
        
    def get_total_tokens(self):
        logger.debug(f"Current tokens: {self.total_tokens}")
        return self.total_tokens

    def summarize_conversation(self, client):
        # Create a prompt from the conversation history
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])
        
        logger.debug(f"Prompt: {prompt}")
        # Ask the model for a summary
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "Please summarize the above conversation."}
            ]
        )
        
        # Extract the summary from the response
        summary = response.choices[0].message.content
        
        # Clear history and add summary as new history
        self.clear()
        self.add_message("system", "Below is a summarized conversation.")
        self.add_message("assistant", summary)
        
        return summary


    def check_token_threshold(self, client):
        if self.total_tokens >= self.token_threshold:
            self.summarize_conversation(client)
        
    def get_response(self, user_input, client):
        logger.debug(f"User: {user_input}")

        # Call the OpenAI API with the conversation history
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            response_format={ "type": "json_object" } # this makes it return only one JSON key-value
        )

        logger.debug(f"Model answer: {response.choices[0].message.content}")

        #total_tokens = conversation.get_total_tokens()
        self.check_token_threshold(client)
        
        return response.choices[0].message.content
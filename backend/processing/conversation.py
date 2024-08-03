import tiktoken

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
        print("curr tokens", self.total_tokens)
        return self.total_tokens

    def summarize_conversation(self, client):
        # Create a prompt from the conversation history
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])
        
        print("Prompt",prompt)
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
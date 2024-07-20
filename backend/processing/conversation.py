import tiktoken

# Initialize encoder
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

class Conversation:
    def __init__(self):
        self.history = [
            {"role": "system", "content": "You are a tech interviewer helper you must help the interviewee. Output your response in JSON"}
        ]
        self.total_tokens = 0

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
import tiktoken

'''
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
'''

def num_tokens(message, model_name):
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(message))
    return num_tokens

# def add_message(message):

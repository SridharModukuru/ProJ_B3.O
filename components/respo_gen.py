# voice_assistant/response_generation.py

from groq import Groq
import logging

chat_history = [
    {"role": "system", "content": """ You are a helpful Assistant called Verbi. 
        You are friendly and fun and you will help the users with their requests.
        Your answers are short and concise. """}
]

api_key = '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'

def generate_response(api_key, chat_history):
    """
    Generate a response using Groq.
    
    Args:
    api_key (str): The API key for the Groq service.
    chat_history (list): The chat history as a list of messages.

    Returns:
    str: The generated response text.
    """
    print('Working on responce_gen ...')
    try:
        # Initialize the Groq client
        client = Groq(api_key=api_key)
        
        # Generate response using Groq
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Replace with your Groq model identifier if needed
            messages=chat_history
        )
        
        # Return the generated response
        return response.choices[0].message.content
    
    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        return "Error in generating response"

# generate_response(api_key,chat_history)
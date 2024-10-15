from deepgram import DeepgramClient, SpeakOptions

def text_to_speech(api_key, text, output_file_path):
    """
    Convert text to speech using Deepgram TTS with SSML for special effects.
    
    Args:
    api_key (str): The API key for Deepgram.
    text (str): The SSML text to convert to speech.
    output_file_path (str): The path to save the generated speech audio file.
    """
    try:
        print('Working... on tts ...')
        
        # Initialize Deepgram client
        client = DeepgramClient(api_key=api_key)
        
        # Define TTS options
        options = SpeakOptions(
            model="aura-arcas-en",  # Choose the model you prefer
            encoding="linear16",
            container="wav"
        )
        

        # Make the TTS request
        response = client.speak.v("1").save(output_file_path, {"text": text}, options)
        
        # Confirm the file was saved
        return f"Audio saved to {output_file_path}"

    except Exception as e:
        return f"Failed to convert text to speech: {e}"

# Example usage
text_to_speech('fa514b70902b8a222eadfacf4920d2e0252be990', "Hello, I am peter. I'll help you learning english. what shall we start with , is there any topic that you wanna talk or learn about?", r'C:\Users\Sridhar\_EMPTY FOLDERS\ProJ_B3.O\intro.wav')

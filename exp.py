import requests

# Constants
# API_KEY = 'fa514b70902b8a222eadfacf4920d2e0252be990'
# AUDIO_FILE_PATH = r'C:\Users\Sridhar\_EMPTY FOLDERS\ProJ_B3.O\audio.aac'
URL = 'https://api.deepgram.com/v1/listen'

# Function to transcribe audio
def transcribe_audio(file_path, api_key):
    try:
        with open(file_path, 'rb') as audio_file:
            headers = {
                'Authorization': f'Token {api_key}',
                'Content-Type': 'audio/aac'
            }
            response = requests.post(URL, headers=headers, files={'file': audio_file})

            if response.status_code == 200:
                result = response.json()
                transcription = result.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')
                return transcription
            else:
                return f'Error: {response.status_code} - {response.text}'
    except Exception as e:
        return f'Exception occurred: {e}'

# Execute function
# transcription_result = transcribe_audio(AUDIO_FILE_PATH, API_KEY)
# print(transcription_result)

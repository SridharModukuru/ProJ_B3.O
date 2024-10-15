
from components.transcription import transcribe_audio
from components.responce_gen import generate_response
from components.tts import text_to_speech

chat_history = [
    {"role": "system", "content": """ You are a English Communication voice chatbot called peter. 
        You have to reply very short and sweet. """},
    {"role":"assistant","content":"Hello, I am peter. I'll help you learning english. what shall we start with , is there any topic that you wanna talk or learn about?"}
]


def run_pipeline(responce_text):

    # user_input = transcribe_audio('fa514b70902b8a222eadfacf4920d2e0252be990',r'C:\Users\Sridhar\_EMPTY FOLDERS\ProJ_B3.O\uploads\recording.wav')
    # print('userinput: ',user_input)
    # chat_history.append({"role": "user", "content": user_input})
    # responce_text = generate_response('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',chat_history)
    # print('responce: ',responce_text)
    # chat_history.append({"role": "assistant", "content": responce_text})
    text_to_speech('fa514b70902b8a222eadfacf4920d2e0252be990',responce_text,r'C:\Users\Sridhar\_EMPTY FOLDERS\ProJ_B3.O\static\output.wav')

    return True
# run_pipeline()
# print('w')
from flask import Flask, render_template, request, jsonify
from pipeline import run_pipeline
from flask_cors import CORS
import os

from components.transcription import transcribe_audio
from components.responce_gen import generate_response
from components.tts import text_to_speech

chat_history = [
    {"role": "system", "content": """ You are a English Communication voice chatbot called peter. 
        You have to reply short and sweet. """},
    {"role":"assistant","content":"Hello, I am peter. I'll help you learning english. what shall we start with , is there any topic that you wanna talk or learn about?"}
]

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FILE = 'static/output.wav'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filepath = os.path.join(UPLOAD_FOLDER, 'recording.wav')
    file.save(filepath)

    # Run the pipeline and check if it was successful
    user_input = transcribe_audio('fa514b70902b8a222eadfacf4920d2e0252be990',r'C:\Users\Sridhar\_EMPTY FOLDERS\ProJ_B3.O\uploads\recording.wav')
    # create div on right part with color blue and right align it and display user_input in it
    chat_history.append({"role": "user", "content": user_input})
    responce_text = generate_response('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',chat_history)
    chat_history.append({"role": "assistant", "content": responce_text})
    # create div on right part with color grey and left align it and display responce_text

    success = run_pipeline(responce_text)


    if success:
        # Ensure the output file is always available
        return jsonify({'message': 'File successfully processed', 'output': '/static/output.wav'})
    else:
        return jsonify({'error': 'Processing failed'})

if __name__ == '__main__':
    app.run(debug=True)

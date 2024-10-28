from flask import Flask, render_template, request, jsonify, session
from components.responce_gen import generate_response
from components.resp_gen import generate_response_

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management



chat_history = [
    {"role": "system", "content": """You are a Discussion generator. Suppose if the topic is Global warming. 
        Three participants, Ben, Tony, and Steeve, will discuss the topic in a structured way.
     just one exchange each

     for example:
     Ben : hello everyone, our topic today is Global warming and my thoughts on global warming are ...
     Tony: I agree with you Ben. We can reduce it by taking preventive measures.
     Steeve: My opinion is to plant trees...

     end this here, just one chance for each.
     most importantly everyone must definitely respond.
     now the topic is:{}
"""}
]
@app.route('/')
def home():
    return render_template('home2.html')


@app.route('/group')
def index():
    return render_template('app_index.html')

@app.route('/group/start_discussion', methods=['POST'])
def start_discussion():
    topic = request.form['topic']
    chat_history[0]["content"] = chat_history[0]["content"].format(topic)
    
    response_text = generate_response('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', chat_history)
    
    session['ben_output'] = response_text['ben']
    session['tony_output'] = response_text['tony']
    session['steeve_output'] = response_text['steeve']
    
    return jsonify({
        'ben_output': session['ben_output'],
        'tony_output': session['tony_output'],
        'steeve_output': session['steeve_output']
    })

@app.route('/group/get_response', methods=['POST'])
def get_response():
    
    user_input_ = request.form['user_input']
    

    ben_output = session.get('ben_output')
    tony_output = session.get('tony_output')
    steeve_output = session.get('steeve_output')

    suggestion_dict = [
        {'role': 'system', 'content': 'you are a vocabulary and grammar expert who upgrades the user inputs without changing or opposing that,just upgrade the sentence in terms of sentence formation. and most importantly give the responce in form of html structure that can be placed inside a div, Example: user: playing games is a good thing as it is good for health. responce:<b>in my opinion playing is really good for our physical health and there are also a lot of benifits.</b> example2: user: Global warming is good for earth suggestion: in my opinion, global warming is the Greatest thing that can happend to earth.'},
        {'role': 'assistant', 'content': f"ben: {ben_output} tony: {tony_output} steeve: {steeve_output}"},
        {'role': 'user', 'content': f"user: {user_input_}"}
    ]


    suggestion = generate_response_('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', suggestion_dict)
    

    new_chat_history = [
        {
            "role": "system",
            "content": f"""You are continuing a group discussion based on the following responses,responces must not exceed 3-4 sentences for each.:
            Ben: {ben_output}
            Tony: {tony_output}
            Steeve: {steeve_output}
            User: {user_input_}
            Continue the discussion with one response each for Ben, Tony, and Steeve."""
        }
    ]
    
    
    response_text = generate_response('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', new_chat_history)
    
    session['ben_output'] = response_text['ben']
    session['tony_output'] = response_text['tony']
    session['steeve_output'] = response_text['steeve']
    
    return jsonify({
        'ben_output': session['ben_output'],
        'tony_output': session['tony_output'],
        'steeve_output': session['steeve_output'],
        'user_suggestion': suggestion
    })


from flask import Flask, render_template, request, jsonify
# from pipeline import run_pipeline
from flask_cors import CORS
import os
import asyncio

from components.transcription import transcribe_audio
from components.respo_gen import generate_response___
from components.tts import text_to_speech

chat_history_ = [
    {"role": "system", "content": """ You are an English Communication voice chatbot called Peter. 
        You have to reply very short(just in two or three sentences) and sweet. """},
    {"role":"assistant", "content":"Hello, I am Peter. I'll help you learn English. What shall we start with? Is there any topic you'd like to talk or learn about?"}
]

# app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FILE = 'static/output.wav'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/chat')
def indexx():
    return render_template('index.html')

@app.route('/chat/upload', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, 'recording.wav')
    file.save(filepath)

    # Transcribe the audio asynchronously
    user_input = await asyncio.to_thread(transcribe_audio, 'ddbf32fde2fa328ab0f486c251de09ce1492be6d', filepath)

    if not user_input.strip():  # Check if transcription is empty
        return jsonify({'error': 'No voice detected'}), 400

    print(user_input)
    chat_history_.append({"role": "user", "content": user_input})


    response_text = await asyncio.to_thread(generate_response___, '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', chat_history_)
    print(response_text)


    output_file = os.path.join('static', 'output.wav')
    await text_to_speech('fa514b70902b8a222eadfacf4920d2e0252be990', response_text, output_file)

    chat_history_.append({"role": "assistant", "content": response_text})

    # Return the transcription and the audio URL
    return jsonify({
        'message': user_input,
        'response': response_text,
        'audio_url': f'/static/output.wav'
    }), 200

# _____________________  from here_________:slide.py
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from components.extract_images import extract_text_and_images_from_pptx
from components.generate_content import process_images

UPLOAD_FOLDER__ = 'uploaded_files'
IMAGE_FOLDER__ = 'slide_images'
ALLOWED_EXTENSIONS = {'pptx'}

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER__
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER__
app.config['API_KEY'] = "AIzaSyC88AWwQQiL8_ZYWkmfIut5MnxkfiOYqt4"
app.config['MODEL_NAME'] = "gemini-1.5-flash"

# Ensure upload and image directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file has a valid extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/slide')
def index_():
    return render_template('slide_index.html')
@app.route('/slide/upload', methods=['POST'])
def upload_slide_file():
    if 'file' not in request.files:
        return redirect(url_for('index_'))

    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract images and text from the PPTX file
        extracted_data = extract_text_and_images_from_pptx(file_path, app.config['IMAGE_FOLDER'])

        # Prepare the prompt for the Gemini model
        prompt_template = """You are a smart AI assistant generating elaborate content for giving a presentation based on the images and text present in the slide.
            Elaborate the content of the slide in a specific manner.
            For example, if the text in the slide is: Rose, Hibiscus, Lily and the images are of these flowers, you should explain like:
            1. This beautiful flower: Rose, is red in color and the most beautiful flower.
            2. The next one, Hibiscus, is ...
            Relate the images and text and form a continuous flow of the presentation.
            No need for introduction unless the text asks for it.
            Now, the text is: {text}
        """
         
        results = []
        count = 0
        for slide_data in extracted_data:
            text = slide_data['text']
            count += 1

            # Modify the prompt based on slide position
            if count == 1:
                text = 'This is the first slide, start by wishing and introducing the topic and slowly get into the text: ' + text
            if count == len(extracted_data):
                text = 'Finally, ' + text + ' thank you.'

            prompt = prompt_template.format(text=text)
            images_folder = slide_data['images']
            
            # Process images and get the response
            slide_results = process_images(app.config['API_KEY'], app.config['MODEL_NAME'], images_folder, prompt)
            results.append(slide_results)
        
        return render_template('result.html', results=results)

    return redirect(url_for('index_'))

if __name__ == '__main__':
    app.run(debug=True)

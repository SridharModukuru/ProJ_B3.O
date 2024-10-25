import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from components.extract_images import extract_text_and_images_from_pptx
from components.generate_content import process_images


UPLOAD_FOLDER = 'uploaded_files'
IMAGE_FOLDER = 'slide_images'
ALLOWED_EXTENSIONS = {'pptx'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['API_KEY'] = "AIzaSyC88AWwQQiL8_ZYWkmfIut5MnxkfiOYqt4"
app.config['MODEL_NAME'] = "gemini-1.5-flash"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('slide_index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract images and text from the PPTX file
        extracted_data = extract_text_and_images_from_pptx(file_path, app.config['IMAGE_FOLDER'])

        # Prepare the prompt for the Gemini model
        prompt_template = """You are smart ai assistant that generates the elobarates content for giving a presentation by providing images and the text present in the slide,
            elobarate the content of the slide in such a way that it is in a specific manner.
            for example: if the text in the slide is: Rose Hibiscus Lily and the images are of these flowers, you should explain like
            1.take a this beautiful flower: Rose, it is red in color and the most beautiful flower.
            2.and the next one is hibisus is ....
            3...   in this way you how to think about the pictures and text, relate them and form a continuous flow of presentation.
            no need of introduction as you are in the middle of presentation unless the text is asking for it.
            Give the responce in continuous normal text without any effects, as new line or special characters might result in ** and /n 
            now the text is : {text}
        """
         
        results = []
        count = 0
        for slide_data in extracted_data:
            text=slide_data['text']
            count += 1
            if count == 1:
                text = 'This is first slide, start by wishing and introducing the topic and slowly get into this text:'+text
            if count == len(extracted_data):
                text = 'Finally'+text+'thank you.'

            prompt = prompt_template.format(text=text)
            images_folder = slide_data['images']
            slide_results = process_images(app.config['API_KEY'], app.config['MODEL_NAME'], images_folder, prompt)
            print("==========================================================================")
            print(slide_results)
            print("==========================================================================")
            results.append(slide_results)
        
        return render_template('result.html', results=results)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

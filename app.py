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
     now the topic is:{}
"""}
]

@app.route('/')
def index():
    return render_template('app_index.html')

@app.route('/start_discussion', methods=['POST'])
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

@app.route('/get_response', methods=['POST'])
def get_response():
    
    user_input = request.form['user_input']
    

    ben_output = session.get('ben_output')
    tony_output = session.get('tony_output')
    steeve_output = session.get('steeve_output')

    suggestion_dict = [
        {'role': 'system', 'content': 'Suggestion should be very small and definitely follow tha Html structure.1.you are a professional english teacher who suggests the better way to convey their responce in a group discussion politely. Suggestion details and reasons in structured HTML.'},
        {'role': 'assistant', 'content': f"ben: {ben_output} tony: {tony_output} steeve: {steeve_output}"},
        {'role': 'user', 'content': f"user: {user_input}"}
    ]


    suggestion = generate_response_('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', suggestion_dict)
    

    new_chat_history = [
        {
            "role": "system",
            "content": f"""You are continuing a group discussion based on the following responses:
            Ben: {ben_output}
            Tony: {tony_output}
            Steeve: {steeve_output}
            User: {user_input}
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

if __name__ == '__main__':
    app.run(debug=True)

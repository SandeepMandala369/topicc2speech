from flask import Flask, request, render_template
import os
from dotenv import load_dotenv

# Import our custom modules for text generation and TTS
import generate_text
import tts

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY not set in .env file")
# Set the OpenAI API key for the client library
# (The generate_text module will use openai.api_key internally)
import openai
openai.api_key = openai_api_key

@app.route('/', methods=['GET'])
def index():
    """Home page with a form to input the main topic."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle the main topic form submission: generate overview text and audio."""
    topic = request.form['topic'].strip()
    # Get overview text from OpenAI
    overview_text = generate_text.generate_overview(topic)
    # Convert overview text to speech (save to static/audio/overview.wav)
    audio_path = 'audio/overview.wav'
    tts.text_to_speech(overview_text, os.path.join('static', audio_path))
    # Render the result page with the overview and subtopic options
    return render_template('result.html', 
                           topic=topic, 
                           overview_text=overview_text, 
                           overview_audio=audio_path)

@app.route('/subtopic', methods=['POST'])
def subtopic():
    """Handle a subtopic selection: generate subtopic-focused text and audio."""
    topic = request.form['topic']
    overview_text = request.form['overview_text']
    subtopic_choice = request.form['subtopic']
    # Get subtopic-specific text from OpenAI
    subtopic_text = generate_text.generate_subtopic(topic, subtopic_choice)
    # Convert subtopic text to speech (save to static/audio/subtopic.wav)
    sub_audio_path = 'audio/subtopic.wav'
    tts.text_to_speech(subtopic_text, os.path.join('static', sub_audio_path))
    # Render the same result page, now including the subtopic section
    return render_template('result.html', 
                           topic=topic, 
                           overview_text=overview_text, 
                           overview_audio='audio/overview.wav',
                           subtopic=subtopic_choice, 
                           subtopic_text=subtopic_text, 
                           subtopic_audio=sub_audio_path)

# Run the app (for development use). In production, use a WSGI server.
if __name__ == '__main__':
    app.run(debug=True)

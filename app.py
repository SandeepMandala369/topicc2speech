from flask import Flask, render_template, request, redirect, url_for
import generate_text
import tts

app = Flask(__name__)

@app.route('/')
def index():
    # Render the topic input form
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    """
    Receives POST data:
      - topic (hidden or from initial form)
      - subtopics (checkboxes)
    Generates text combining topic + subtopics,
    converts to speech, and displays result.
    """
    topic = request.form.get('topic')
    if not topic:
        # If no topic found, redirect to start a new topic
        return redirect(url_for('index'))

    # Collect the selected subtopics from the checkboxes
    subtopics = request.form.getlist('subtopics')

    # Generate text
    generated_text = generate_text.generate_text(topic, subtopics)

    # Convert the text to speech
    audio_file = tts.text_to_speech(generated_text)

    return render_template('result.html',
                           topic=topic,
                           text=generated_text,
                           selected_subtopics=subtopics,
                           audio_file=audio_file)

if __name__ == '__main__':
    app.run(debug=True)

import os
import uuid
from gtts import gTTS

BASE_DIR = os.path.dirname(__file__)
AUDIO_DIR = os.path.join(BASE_DIR, 'static', 'audio')

def text_to_speech(text: str) -> str:
    """
    Convert the given text into speech, 
    save as an mp3 file, and return the relative path.
    """
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)

    # Generate TTS with gTTS
    tts = gTTS(text)
    tts.save(file_path)

    # Return relative path (Flask serves from 'static/')
    return f"audio/{filename}"

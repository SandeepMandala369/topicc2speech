import pyttsx3, os

def text_to_speech(text: str, output_path: str) -> None:
    """Convert the given text to speech and save it to output_path (WAV or MP3)."""
    engine = pyttsx3.init()  # Initialize TTS engine
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Save the speech audio to the specified file
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    # (No explicit return needed; the file is written to disk)

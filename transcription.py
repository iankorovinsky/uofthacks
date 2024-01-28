from openai import OpenAI
import os
import dotenv
from pathlib import Path

global client 
def init():
    global client
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def transcriber(filename):
    directory = f"media/audio/{filename}"
    audio_file= open(directory, "rb")

    print(audio_file)

    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    print(transcript)
    print(f"TRANSCRIPTION: {transcript.text}")
    return transcript.text
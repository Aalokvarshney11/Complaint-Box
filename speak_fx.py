import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

def speak(text):
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id="eleven_multilingual_v2"
    )
    audio_bytes = b"".join(audio)
    return audio_bytes
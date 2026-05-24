from elevenlabs import ElevenLabs
import os

class TTSService:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def text_to_speech(self, text):

        audio = self.client.text_to_speech.convert(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # default voice
            model_id="eleven_multilingual_v2",
            text=text
        )

        return audio
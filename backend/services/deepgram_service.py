from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import os

class DeepgramService:
    def __init__(self):
        self.client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
        self.conn = None

    def start(self, callback):
        self.conn = self.client.listen.websocket.v("1")

        self.conn.on(
            LiveTranscriptionEvents.Transcript,
            callback
        )

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            encoding="mulaw",
            sample_rate=8000,
            channels=1
        )

        self.conn.start(options)

    def send_audio(self, audio):
        if self.conn:
            self.conn.send(audio)
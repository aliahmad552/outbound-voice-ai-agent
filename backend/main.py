from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv
from twilio.rest import Client
import os
import json
import base64
from services.tts_service import TTSService


from services.deepgram_service import DeepgramService
from services.groq_service import GroqService
from core.prompts import SYSTEM_PROMPT

load_dotenv()

app = FastAPI()

# ---------------- TWILIO ----------------
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

# ---------------- SERVICES ----------------
deepgram = DeepgramService()
groq = GroqService()
tts = TTSService()

@app.get("/")
def home():
    return {"status": "Voice AI Running"}


# ---------------- WEB SOCKET ----------------
@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):

    await websocket.accept()
    print("WebSocket Connected")

    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    def handle_transcript(self, result, **kwargs):
        text = result.channel.alternatives[0].transcript

        if text:
            print("USER:", text)

            conversation.append({
                "role": "user",
                "content": text
            })

            reply = groq.get_reply(conversation)

            print("AI:", reply)

            conversation.append({
                "role": "assistant",
                "content": reply
            })

    deepgram.start(handle_transcript)

    while True:
        data = await websocket.receive_text()
        data = json.loads(data)

        if data["event"] == "media":
            audio = base64.b64decode(data["media"]["payload"])
            deepgram.send_audio(audio)


# ---------------- CALL TRIGGER ----------------
@app.get("/make-call")
def make_call():

    TWIML = """
    <Response>
        <Connect>
            <Stream url="wss://subatomic-latticed-gallows.ngrok-free.dev/media-stream"/>
        </Connect>
    </Response>
    """

    call = twilio_client.calls.create(
        to="+923078965638",
        from_=TWILIO_PHONE,
        twiml=TWIML
    )

    return {"status": "calling", "call_sid": call.sid}
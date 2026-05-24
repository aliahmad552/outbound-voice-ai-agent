from fastapi import FastAPI, WebSocket
from twilio.rest import Client
from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from groq import Groq

import os
import json
import base64
import asyncio

load_dotenv()

app = FastAPI()

# =========================
# TWILIO
# =========================

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# =========================
# DEEPGRAM
# =========================

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

deepgram = DeepgramClient(DEEPGRAM_API_KEY)

# =========================
# GROQ
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
You are Sarah, an appointment assistant from Al-Wahab Clinic.

Your responsibilities:
- remind users about appointments
- ask for confirmation
- respond professionally
- keep responses short
"""


@app.get("/")
async def root():
    return {"message": "Voice AI Agent Running"}


@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):

    await websocket.accept()

    print("WebSocket Connected")

    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    dg_connection = deepgram.listen.websocket.v("1")

    async def on_message(self, result, **kwargs):

        sentence = result.channel.alternatives[0].transcript

        if sentence:

            print("\nCustomer:", sentence)

            conversation_history.append({
                "role": "user",
                "content": sentence
            })

            # =========================
            # GROQ RESPONSE
            # =========================

            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=conversation_history
            )

            ai_reply = response.choices[0].message.content

            print("\nAI:", ai_reply)

            conversation_history.append({
                "role": "assistant",
                "content": ai_reply
            })

    dg_connection.on(
        LiveTranscriptionEvents.Transcript,
        on_message
    )

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        encoding="mulaw",
        channels=1,
        sample_rate=8000
    )

    dg_connection.start(options)

    while True:

        data = await websocket.receive_text()

        data = json.loads(data)

        if data["event"] == "media":

            media_data = data["media"]["payload"]

            chunk = base64.b64decode(media_data)

            dg_connection.send(chunk)


@app.get("/make-call")
async def make_call():

    twiml = """
    <Response>
        <Connect>
            <Stream url="wss://subatomic-latticed-gallows.ngrok-free.dev/media-stream" />
        </Connect>
    </Response>
    """

    call = twilio_client.calls.create(
        to="+923078965638",
        from_=TWILIO_PHONE,
        twiml=twiml
    )

    return {"status": "calling"}
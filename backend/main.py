from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from twilio.rest import Client

import os
import json
import base64
import asyncio

from services.deepgram_service import DeepgramService
from services.llm_service import LLMService
from core.prompts import SYSTEM_PROMPT

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

# =========================================================
# FASTAPI
# =========================================================

app = FastAPI()

# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="backend/static"),
    name="static"
)

# =========================================================
# TWILIO CLIENT
# =========================================================

twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

# =========================================================
# SERVICES
# =========================================================

deepgram = DeepgramService()
llm_service = LLMService()

# =========================================================
# FRONTEND
# =========================================================

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

# =========================================================
# REQUEST MODEL
# =========================================================

class CallRequest(BaseModel):
    phone_number: str
    scenario: str

# =========================================================
# WEBSOCKET MEDIA STREAM
# =========================================================

@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):

    await websocket.accept()

    print("WebSocket Connected")

    # Conversation memory
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # =====================================================
    # HANDLE TRANSCRIPT
    # =====================================================

    async def handle_transcript(self, result, **kwargs):

        try:

            text = result.channel.alternatives[0].transcript

            # Ignore empty transcripts
            if not text or not text.strip():
                return

            print(f"\nUSER: {text}")

            # Add user message
            conversation.append({
                "role": "user",
                "content": text
            })

            # =================================================
            # LLM RESPONSE
            # =================================================

            reply = llm_service.get_reply(conversation)

            print(f"\nAI: {reply}")

            # Add AI reply to memory
            conversation.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:
            print("Transcript Error:", e)

    # =====================================================
    # START DEEPGRAM
    # =====================================================

    deepgram.start(
        lambda *args, **kwargs:
        asyncio.create_task(
            handle_transcript(*args, **kwargs)
        )
    )

    # =====================================================
    # RECEIVE AUDIO FROM TWILIO
    # =====================================================

    try:

        while True:

            data = await websocket.receive_text()

            data = json.loads(data)

            event = data.get("event")

            # ---------------------------------------------
            # MEDIA EVENT
            # ---------------------------------------------

            if event == "media":

                media_payload = data["media"]["payload"]

                audio = base64.b64decode(media_payload)

                deepgram.send_audio(audio)

            # ---------------------------------------------
            # CONNECTED EVENT
            # ---------------------------------------------

            elif event == "connected":
                print("Twilio Connected")

            # ---------------------------------------------
            # START EVENT
            # ---------------------------------------------

            elif event == "start":
                print("Streaming Started")

            # ---------------------------------------------
            # STOP EVENT
            # ---------------------------------------------

            elif event == "stop":
                print("Streaming Stopped")
                break

    except Exception as e:
        print("WebSocket Error:", e)

# =========================================================
# MAKE CALL
# =========================================================

@app.post("/make-call")
def make_call(call_request: CallRequest):

    try:

        TWIML = """
        <Response>
            <Connect>
                <Stream url="wss://YOUR_NGROK_URL/media-stream"/>
            </Connect>
        </Response>
        """

        call = twilio_client.calls.create(
            to=call_request.phone_number,
            from_=TWILIO_PHONE,
            twiml=TWIML
        )

        return {
            "status": "calling",
            "scenario": call_request.scenario,
            "call_sid": call.sid
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
from fastapi import FastAPI
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# twilio credentials
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

print(TWILIO_PHONE)
print(ACCOUNT_SID,AUTH_TOKEN)
@app.get("/")
async def root():
    return {"messages":"voice ai agent is running"}


@app.get("/make-call")
async def make_call():
    call = client.calls.create(
        to='+923078965638',
        from_=TWILIO_PHONE,
        twiml = """
        <Response>
            <Say>Hello Ali, this is your AI voice agent. </Say>
        </Response>
        """
    )

    return {
        'status':'calling',
        'call_sid':call.sid
    }
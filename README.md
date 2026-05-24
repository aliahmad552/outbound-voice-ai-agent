# Voice AI Agent – Outbound Calling System

## Overview

This project is a real-time Voice AI Agent built using FastAPI, Twilio, Deepgram, Groq, LangChain, and ElevenLabs.

The system is capable of:

- Making outbound phone calls
- Streaming live audio through WebSockets
- Converting speech to text in real-time
- Generating intelligent AI responses
- Maintaining conversation context
- Converting AI responses into voice

The project demonstrates a production-minded Voice AI architecture by combining telephony, speech processing, LLM reasoning, and real-time communication.

---

# Implemented Scenario

## Appointment Reminder & Confirmation

The AI assistant calls users to:

- Remind them about appointments
- Ask for confirmation
- Handle simple conversational responses naturally

### AI Persona

**Name:** Sarah

Sarah is a polite and professional AI appointment assistant.

### Example Conversation

```text
AI: Hello, this is Sarah from ABC Clinic. I am calling to remind you about your appointment tomorrow at 3 PM.

User: Okay.

AI: Would you like to confirm your appointment?

User: Yes.

AI: Great. Your appointment has been confirmed. Thank you.
```

# Teck Stack
```bash

| Layer               | Technology |
| ------------------- | ---------- |
| Backend Framework   | FastAPI    |
| Telephony           | Twilio     |
| Speech-to-Text      | Deepgram   |
| LLM                 | Groq       |
| LLM Orchestration   | LangChain  |
| Text-to-Speech      | ElevenLabs |
| Real-Time Streaming | WebSockets |
| Tunneling           | Ngrok      |
```

# System Architecture

```bash

                 ┌─────────────────────┐
                 │     Frontend UI     │
                 │  Phone + Scenario   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 │   Call Controller   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Twilio        │
                 │  Outbound Calling   │
                 └──────────┬──────────┘
                            │
                     Live Audio Stream
                            │
                            ▼
                 ┌─────────────────────┐
                 │ FastAPI WebSocket   │
                 │  Audio Receiver     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Deepgram       │
                 │   Speech-to-Text    │
                 └──────────┬──────────┘
                            │
                       Transcript
                            │
                            ▼
                 ┌─────────────────────┐
                 │ LangChain + Groq    │
                 │   AI Reasoning      │
                 └──────────┬──────────┘
                            │
                       AI Response
                            │
                            ▼
                 ┌─────────────────────┐
                 │    ElevenLabs       │
                 │   Text-to-Speech    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Twilio         │
                 │  Voice Playback     │
                 └─────────────────────┘

```


# Project Structure

```bash

voice-ai-agent/
│
├── backend/
│   ├── main.py
│   │
│   ├── services/
│   │   ├── deepgram_service.py
│   │   ├── llm_service.py
│   │   ├── tts_service.py
│   │
│   ├── core/
│   │   ├── prompts.py
│   │
│   ├── static/
│   │   ├── index.html
│   │
│   ├── .env
│   ├── requirements.txt
│
└── README.md

```

# Features
## Implemented Features
- Outbound calling using Twilio
- Real-time audio streaming using WebSockets
- Speech-to-text using Deepgram
- AI conversation using Groq + LangChain
- Context-aware conversation history
- Modular service-based architecture
- Minimal frontend UI
- FastAPI backend
- Dynamic scenario support
## Frontend UI

The frontend is a minimal single-page interface where users can:

- Enter a phone number
- Select a scenario
- Trigger an outbound call

This satisfies the minimal UI requirement of the assignment.

## Backend Design

The backend is built completely using FastAPI.

**Major Components**
### 1. FastAPI REST Endpoints

Used for:

Triggering calls
Serving frontend
Managing APIs
### 2. FastAPI WebSocket

Used for:

Receiving live Twilio audio
Real-time streaming
Low-latency communication
### 3. Deepgram Service

Responsible for:

Receiving audio chunks
Performing live transcription
### 4. LangChain + Groq

Responsible for:

Prompt handling
Conversation memory
AI response generation
### 5. ElevenLabs

Responsible for:

Converting AI text into realistic speech

# Conversation Flow

```text
1. User enters phone number
2. FastAPI triggers outbound Twilio call
3. Twilio streams audio to FastAPI WebSocket
4. Audio is forwarded to Deepgram
5. Deepgram returns transcript
6. Transcript is passed to LangChain + Groq
7. AI generates contextual response
8. Response is converted into voice using ElevenLabs
9. Voice is streamed back to the user

```

### Why LangChain Was Used

LangChain was used to:

- Standardize prompt formatting
- Maintain conversation structure
- Keep the LLM layer modular
- Make switching between models easier

This design allows future integration with:

- OpenAI
- Claude
- Gemini
- Open-source models

without changing the core application logic.

## Scalability Considerations

The architecture was intentionally designed to be modular and scalable.

### Future Improvements
- Multi-agent workflows
- Database integration
- Call analytics
- CRM integration
- Conversation storage
- Voice interruption handling
- Better audio optimization
- Deployment on cloud infrastructure
- Docker support
- Redis queues

## Setup Instructions
### 1. Clone Repository
```bash
git clone <your_repo_url>
cd voice-ai-agent
```
### 2. Create Virtual Environment
```bash
python -m venv .venv
```
### Activate environment:

**Windows**
```bash
.venv\Scripts\activate
```
**Linux / Mac**
```bash
source .venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
**Environment Variables**

Create a .env file:
```bash
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number

DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
ELEVENLABS_API_KEY=your_key
```
**Run Backend**
```bash
uvicorn backend.main:app --reload
```
Start Ngrok
```bash
ngrok http 8000
```
Copy the generated public URL and update the Twilio stream URL.

Example:
```bash
wss://abcd.ngrok-free.app/media-stream
```
**Open Application**
```bash
http://127.0.0.1:8000
```

## API Endpoints

```bash
| Endpoint        | Method    | Description           |
| --------------- | --------- | --------------------- |
| `/`             | GET       | Frontend UI           |
| `/make-call`    | POST      | Trigger outbound call |
| `/media-stream` | WebSocket | Twilio audio stream   |

```

## Design Decisions
### Why FastAPI?
- High performance
- Native WebSocket support
- Async architecture
- Production-friendly
### Why Deepgram?
- Low latency transcription
- Real-time streaming support
- Optimized for conversational AI
### Why Groq?
- Extremely fast inference
- Low response latency
- Strong conversational performance
### Why Twilio?
- Reliable telephony APIs
- Real-time media streaming
- Industry-standard voice infrastructure
### Challenges Faced

During development, several real-world engineering challenges were addressed:

- Twilio trial restrictions
- WebSocket streaming setup
- Audio encoding compatibility
- Deepgram SDK version conflicts
- Real-time event handling
- Conversation state management

These challenges helped improve the production-readiness of the architecture.

## Future Enhancements
- Full duplex audio streaming
- Interrupt handling
- Better memory management
- Voice activity detection
- Human handoff system
- Analytics dashboard
- Authentication
- Database support
-Deployment pipeline
## Conclusion

This project demonstrates a production-minded Voice AI architecture using modern AI and telephony services.

The system combines:

- Telephony
- Real-time streaming
- Speech processing
- LLM reasoning
- Voice synthesis

into a modular and scalable conversational AI system.

The architecture is designed to be extensible, maintainable, and suitable for future enterprise-grade improvements.
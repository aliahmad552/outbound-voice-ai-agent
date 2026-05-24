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
# 🤖 AI-Calendar-Agent

AI‑Calendar‑Agent is an intelligent, conversational application that automates Google Calendar management via natural language. Built with Python (FastAPI backend and Streamlit frontend), it helps users create, modify, and view calendar events through chat-like interactions.

---

## 🗓️ Features

- **Natural Language Interface**  
  Describe your scheduling needs (e.g. "Schedule a 30-minute stand-up tomorrow at 10 AM with Sara") and let the agent parse dates, times, attendees, and intent.

- **Availability Checking**  
  Before booking, the agent checks your Google Calendar to avoid conflicts, providing suggestions or requesting alternatives.

- **Multi-Step Interaction**  
  Supports follow-up dialogues for missing details (e.g. verifying time zone, attendee list, or location).

- **Event Management**  
  - Create new events  
  - Modify or reschedule existing events  
  - Review upcoming events or specific date ranges

---

## ⚙️ Tech Stack

| Component | Details |
|----------|---------|
| Backend  | FastAPI (Python) |
| Agent Logic | Custom NLU + Calendar utilities |
| Frontend | Streamlit (chat-style interface) |
| Calendar API | Google Calendar via OAuth2 |
| Language Understanding | OpenAI GPT for parsing user input |

---

## 🧩 Project Structure


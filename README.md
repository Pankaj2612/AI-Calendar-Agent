# 🤖 AI Calendar Agent

**AI Calendar Agent** is an intelligent, conversational assistant that helps users schedule, update, and manage **Google Calendar** events using **natural language**. Built with **Python (FastAPI + Streamlit)** and powered by **OpenAI**, it automates calendar operations like booking, checking availability, and updating events — all through a simple chat interface.

---

## ✨ Features

- 🗣️ **Conversational Scheduling**  
  Schedule events like "Book a meeting with John tomorrow at 3 PM" using plain English.

- 📆 **Google Calendar Integration**  
  Full integration to:
  - Create new events  
  - Check your availability  
  - Modify existing events  
  - Prevent overlaps

- 🧠 **Context-Aware Agent**  
  Uses OpenAI's GPT model to extract:
  - Date & time  
  - Attendees  
  - Duration  
  - Intent (create, update, etc.)

- 🔁 **Interactive Dialogues**  
  Agent asks follow-up questions if your input is missing details — just like a real assistant!

- 💬 **User-Friendly Interface**  
  Clean, minimal frontend built using **Streamlit** for a chat-like experience.

---

## 🛠️ Tech Stack

| Layer       | Tech                            |
|-------------|----------------------------------|
| Backend     | Python, FastAPI                 |
| Frontend    | Streamlit                       |
| NLP Engine  | OpenAI GPT (via API)            |
| Calendar API| Google Calendar API (OAuth2)    |
| Auth        | Google OAuth2 Client Credentials|

---

## 🧩 Project Structure

```
AI-Calendar-Agent/
├── backend/
│   ├── app.py               # FastAPI app entry point
│   ├── calendar_utils.py    # Google Calendar API helpers
│   └── credentials.json     # Your Google OAuth credentials
│
├── frontend/
│   └── streamlit_app.py     # Streamlit interface
│
├── agent.py                 # Agent logic (LLM + command handling)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (optional)
└── README.md                # Full documentation
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- OpenAI API Key
- Google Cloud Project with Calendar API enabled

---

## 🔐 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Pankaj2612/AI-Calendar-Agent.git
cd AI-Calendar-Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **Google Calendar API**.
3. Create OAuth 2.0 credentials (type: Desktop).
4. Download the `credentials.json` and place it inside `backend/`.

### 5. Set Your OpenAI API Key

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your-openai-key-here
```

Or export it directly:

```bash
export OPENAI_API_KEY=your-openai-key-here
```

---

## ▶️ Running the App

### Start Backend (FastAPI)

```bash
cd backend
uvicorn app:app --reload
```

### Start Frontend (Streamlit)

In a new terminal:

```bash
cd frontend
streamlit run streamlit_app.py
```

- Visit: `http://localhost:8501`

---

## 💬 Example Usage

> **User**: Schedule a 45-minute call with Alice and Bob next Friday at 11 AM.  
>  
> **Agent**: You're free at 11 AM on Friday. Should I go ahead and schedule?  
>  
> **User**: Yes.  
>  
> ✅ Event "Call with Alice and Bob" has been added to your Google Calendar.

---

## 🧱 Example `.env` File

```env
OPENAI_API_KEY=your-openai-api-key
```

> ⚠️ Never commit your `.env` or `credentials.json` file to version control.

---

## 🧠 Future Enhancements

- 🔁 Support recurring events
- 🔍 Delete/search calendar entries
- 🌍 Smart timezone handling
- 🔐 User authentication & multi-session support
- 🧪 Add vector search to summarize previous meeting history

---

## 🙋‍♂️ Author

Made with ❤️ by [Pankaj Sahu](https://github.com/Pankaj2612)  
Feedback and contributions are always welcome!

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to fork, use, and build upon it.

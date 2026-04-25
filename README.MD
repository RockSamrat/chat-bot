# 🤖 AI Chatbot — Local LLM with Auth

A locally-running AI chatbot powered by **Ollama + LLaMA 3.2**, with a desktop GUI (Tkinter), a Flask REST API backend, and JWT-based user authentication backed by a **Neon (PostgreSQL)** database.

---

## ✨ Features

- 💬 Chat with LLaMA 3.2 running fully locally via Ollama
- 🔐 User registration & login with JWT authentication
- 🗄️ PostgreSQL (Neon) database with auto-migration on first run
- 🖥️ Clean Tkinter desktop GUI with chat bubbles
- 🔒 Passwords hashed with bcrypt — never stored in plaintext
- 🚪 Logout clears the token from memory immediately

---

## 📁 Project Structure

```
chat-bot/
├── backend/
│   ├── server.py           # Flask API — auth routes + chat proxy
│   ├── auth_model.py       # User CRUD + bcrypt password hashing
│   ├── auth_middleware.py  # JWT create/verify + Flask route decorator
│   ├── db.py               # DB connection pool + migration runner
│   ├── schema.sql          # Neon DB schema (auto-applied on first run)
│   └── main.py             # Ollama LangChain chain (LLaMA 3.2)
├── chat-bot-gui.py         # Tkinter desktop GUI
├── requirements.txt        # Python dependencies
├── .env                    # Secrets (not committed — see below)
└── .gitignore
```

---

## ⚙️ Prerequisites

Make sure you have the following installed:

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- A [Neon](https://neon.tech/) PostgreSQL database (free tier works fine)

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/RockSamrat/chat-bot.git
cd chat-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install psycopg2-binary bcrypt PyJWT python-dotenv flask flask-cors requests langchain-ollama langchain-core
```

### 3. Create your `.env` file

Create a `.env` file in the project root with the following:

```env
DATABASE_URL='your-neon-connection-string'
JWT_SECRET='your-long-random-secret'
FLASK_DEBUG=false
```

> **Generate a secure JWT secret:**
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## ▶️ Running the Application

Open **three separate terminals** and run each step in order:

### Step 1 — Start the Flask backend

```bash
python backend/server.py
```

> This automatically applies the database schema on first boot.

### Step 2 — Start Ollama with LLaMA 3.2

```bash
ollama serve
```

In another terminal (or after `serve` is running):

```bash
ollama run llama3.2
```

> If you haven't downloaded the model yet, this will pull it automatically.

### Step 3 — Launch the GUI

```bash
python chat-bot-gui.py
```

The app will open. **Register** a new account or **Sign in** to start chatting.

---

## 🔌 API Reference

The Flask backend runs at `http://localhost:5000`.

| Method | Endpoint              | Auth Required | Description              |
|--------|-----------------------|:-------------:|--------------------------|
| POST   | `/api/auth/register`  | No            | Create a new account     |
| POST   | `/api/auth/login`     | No            | Login and receive a JWT  |
| GET    | `/api/auth/me`        | Yes ✅        | Verify token / get profile |
| POST   | `/api/chat`           | Yes ✅        | Send a message to the AI |

### Register

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "alice",
  "password": "mypassword123"
}
```

**Response `201`:**
```json
{
  "token": "<jwt>",
  "username": "alice"
}
```

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "alice",
  "password": "mypassword123"
}
```

**Response `200`:**
```json
{
  "token": "<jwt>",
  "username": "alice"
}
```

### Chat (protected)

```http
POST /api/chat
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "question": "Hello!",
  "context": ""
}
```

**Response `200`:**
```json
{
  "response": "Hi! How can I help you today?"
}
```

---

## 🔐 Security Notes

| Concern | How it's handled |
|---|---|
| Passwords | Hashed with **bcrypt** — never stored as plaintext |
| Authentication | **JWT (HS256)** tokens with 24-hour expiry |
| Route protection | All `/api/chat` routes require a valid Bearer token |
| Token storage | Stored **in-memory only** in the GUI — cleared on logout |
| Secret management | `JWT_SECRET` lives only in `.env` — never commit it |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Model | LLaMA 3.2 via Ollama |
| AI Framework | LangChain + langchain-ollama |
| Backend | Flask + Flask-CORS |
| Database | Neon (PostgreSQL) via psycopg2 |
| Auth | bcrypt + PyJWT |
| GUI | Python Tkinter |

---

## 🐛 Troubleshooting

**"Cannot reach server"** — Make sure `python backend/server.py` is running on port 5000.

**"Model not found"** — Run `ollama pull llama3.2` to download the model first.

**Database errors on startup** — Double-check your `DATABASE_URL` in `.env` points to a valid Neon connection string.

**GUI won't open** — Ensure `tkinter` is available. On Linux: `sudo apt install python3-tk`.

---

## 📄 License

This project is open source. Feel free to fork and build on it!
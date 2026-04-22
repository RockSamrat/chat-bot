# AI Chatbot – Authentication Setup Guide

## Project Structure

```
.
├── .env                # Secrets (DATABASE_URL, JWT_SECRET)
├── schema.sql          # Neon DB schema (applied automatically on first run)
├── db.py               # Connection pool + migration runner
├── auth_model.py       # User CRUD + bcrypt password hashing
├── auth_middleware.py  # JWT create/verify + Flask route decorator
├── server.py           # Flask API server (auth + chat proxy)
├── chat-bot-gui.py     # Tkinter GUI (replaces old version)
└── main.py             # Ollama chain (unchanged)
```

## Prerequisites

```bash
pip install psycopg2-binary bcrypt PyJWT python-dotenv flask flask-cors requests langchain-ollama langchain-core
```

## .env Configuration

```
DATABASE_URL='your-neon-connection-string'
JWT_SECRET='generate-a-long-random-secret'
FLASK_DEBUG=false
```

Generate a secure JWT secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Running the Application

**Step 1 – Start the Flask API server** (runs migrations on first boot):
```bash
python server.py
```

**Step 2 – Start Ollama** (in a separate terminal):
```bash
ollama serve
ollama run llama3.2   # pull if not already downloaded
```

**Step 3 – Launch the GUI**:
```bash
python chat-bot-gui.py
```

## API Endpoints

| Method | Path                  | Auth? | Description              |
|--------|-----------------------|-------|--------------------------|
| POST   | /api/auth/register    | No    | Create new account       |
| POST   | /api/auth/login       | No    | Login, receive JWT       |
| GET    | /api/auth/me          | Yes   | Verify token / profile   |
| POST   | /api/chat             | Yes   | Send chat message        |

### Register
```json
POST /api/auth/register
{ "username": "alice", "password": "mypassword123" }

Response 201:
{ "token": "<jwt>", "username": "alice" }
```

### Login
```json
POST /api/auth/login
{ "username": "alice", "password": "mypassword123" }

Response 200:
{ "token": "<jwt>", "username": "alice" }
```

### Chat (protected)
```json
POST /api/chat
Authorization: Bearer <jwt>
{ "question": "Hello!", "context": "" }

Response 200:
{ "response": "Hi! How can I help you today?" }
```

## Security Notes

- Passwords are hashed with **bcrypt** (never stored in plaintext)
- Auth uses **JWT (HS256)** with 24-hour expiry
- All chat routes require a valid JWT
- Token is stored **in-memory only** in the GUI (cleared on logout)
- Add `JWT_SECRET` to your `.env` in production — never commit it
# AI Chatbot System (Flask + Ollama + JWT Authentication)

## Overview

This project is a full-stack AI chatbot application built with a Flask backend and a simple frontend interface. It supports user authentication, AI-powered chat interaction, and persistent conversation storage.

The system demonstrates backend development, authentication, AI integration, and data handling, making it suitable for learning and portfolio purposes.

---

## Features

* User registration and login using JWT authentication
* Protected API routes with middleware
* AI chatbot integration using Ollama
* Conversation history storage
* JSON-based persistence for chats
* Modular backend architecture
* REST API design
* Input validation and error handling

---

## Tech Stack

### Backend

* Python (Flask)
* JWT Authentication
* PostgreSQL (Neon DB for users)
* JSON file storage (chat history)
* Ollama / LangChain (AI model)

### Frontend

* HTML
* CSS
* JavaScript

### Tools

* Git and GitHub
* Linux environment
* Environment variables (.env)

---

## Project Structure

```
chat-bot/
│
├── backend/
│   ├── server.py                # Main Flask application
│   ├── db.py                    # Database connection
│   ├── auth_model.py            # User model logic
│   ├── auth_middleware.py       # JWT middleware
│   ├── conversations.py         # Chat storage logic
│   ├── main.py                  # AI chain (Ollama)
│   └── schema.sql               # Database schema
│
├── frontend/                    # Frontend UI
│
├── conversations.json           # Chat storage (auto-created)
├── requirements.txt
├── .env
└── README.md
```

---

## Authentication Flow

1. User registers via `/api/auth/register`
2. User logs in via `/api/auth/login`
3. JWT token is generated
4. Protected routes verify token using middleware
5. User data is stored in `g.user`

---

## Chat Flow

1. User sends request to `/api/chat`
2. Token is verified
3. Conversation ID is created (if not provided)
4. Previous context is loaded
5. AI model processes the input
6. Response is generated
7. Conversation is saved

---

## Conversation Storage

Chat data is stored in a JSON file:

```
conversations.json
```

### Structure

```json
{
  "conversations": [
    {
      "conversation_id": "uuid",
      "user_id": "123",
      "username": "krish",
      "messages": [
        {
          "role": "user",
          "content": "Hello",
          "timestamp": "ISO"
        },
        {
          "role": "bot",
          "content": "Hi, how can I help?",
          "timestamp": "ISO"
        }
      ]
    }
  ]
}
```

### Notes

* File is created automatically when first message is saved
* Data is appended, not overwritten
* Suitable for learning, not production

---

## API Endpoints

### Authentication

| Method | Endpoint           | Description      |
| ------ | ------------------ | ---------------- |
| POST   | /api/auth/register | Register user    |
| POST   | /api/auth/login    | Login user       |
| GET    | /api/auth/me       | Get user profile |

---

### Chat

| Method | Endpoint  | Description             |
| ------ | --------- | ----------------------- |
| POST   | /api/chat | Send message to chatbot |

---

## Example Request

```bash
curl -X POST http://127.0.0.1:5000/api/chat \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{"question":"Hello"}'
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/RockSamrat/chat-bot.git
cd chat-bot
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment

Create a `.env` file:

```
DATABASE_URL=your_neon_db_url
JWT_SECRET=your_secret_key
PORT=5000
FLASK_DEBUG=true
```

---

### 5. Run Server

```bash
python -m backend.server
```

---

### 6. Run Ollama

Ensure Ollama is running:

```bash
ollama run llama2
```

---

## Common Issues

### conversations.json not created

* Ensure `/api/chat` is called
* Ensure `add_message()` is executed
* Use `"question"` instead of `"message"` in request

---

### Unauthorized error

* Token missing or invalid
* Use correct header:

```
Authorization: Bearer <token>
```

---

### Ollama not working

* Ensure Ollama is installed
* Ensure model is running

---

## Future Improvements

* Replace JSON storage with PostgreSQL
* Add Redis for caching
* Implement WebSocket for real-time chat
* Add UI for chat history
* Containerize using Docker
* Deploy with Kubernetes
* Add CI/CD pipeline

---

## Learning Outcomes

* Backend API development
* Authentication using JWT
* AI integration with LLMs
* Data storage design
* System architecture understanding

---

## License

This project is intended for educational and portfolio use.

# AI Chatbot with Ollama

An AI chatbot powered by Ollama and LangChain, running fully locally on your machine — no internet or API keys needed.

## Features

- Streaming responses with a live typing effect
- Conversation memory (remembers previous messages)
- Response time display
- Exception handling for clean error messages

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed on your machine

## Setup

### 1. Install Ollama

Download and install Ollama from [https://ollama.com](https://ollama.com) and make sure it is running:

```bash
ollama serve
```

### 2. Pull the model

```bash
ollama pull llama3.2
```

### 3. Clone this repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd chat-bot
```

### 4. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the chatbot

```bash
python chatbot.py
```

## Usage

```
Welcome to AI Chatbot! Type 'exit' to quit.

You: What is Python?
Bot: Python is a high-level programming language...
  (responded in 3.21s)

You: exit
Goodbye!
```

## Project Structure

```
├── main.py         # Main chatbot script
├── requirements.txt   # Python dependencies
├── .gitignore         # Files excluded from Git
└── README.md          # This file
```
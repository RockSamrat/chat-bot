"""
json_examples.json - Real-world JSON structure examples
This file shows what stored conversations look like.
"""

# Example 1: Single conversation with 2 message exchanges
{
  "conversations": [
    {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "1",
      "username": "alice_smith",
      "created_at": "2025-04-26T10:30:45.123456",
      "updated_at": "2025-04-26T10:35:20.654321",
      "messages": [
        {
          "role": "user",
          "content": "What is machine learning?",
          "timestamp": "2025-04-26T10:30:45.123456",
          "message_id": "msg-001"
        },
        {
          "role": "bot",
          "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves.",
          "timestamp": "2025-04-26T10:30:52.234567",
          "message_id": "msg-002"
        },
        {
          "role": "user",
          "content": "Can you give me a real-world example?",
          "timestamp": "2025-04-26T10:31:30.345678",
          "message_id": "msg-003"
        },
        {
          "role": "bot",
          "content": "Sure! Email spam filters are a great example. They learn from examples of spam and legitimate emails to automatically classify incoming emails. As you mark emails as spam, the system learns and improves its predictions.",
          "timestamp": "2025-04-26T10:31:40.456789",
          "message_id": "msg-004"
        }
      ]
    }
  ]
}


# Example 2: Multiple conversations from different users
{
  "conversations": [
    {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "1",
      "username": "alice",
      "created_at": "2025-04-26T10:00:00.000000",
      "updated_at": "2025-04-26T10:15:00.000000",
      "messages": [
        {
          "role": "user",
          "content": "Hello!",
          "timestamp": "2025-04-26T10:00:00.000000",
          "message_id": "msg-001"
        },
        {
          "role": "bot",
          "content": "Hello! How can I help today?",
          "timestamp": "2025-04-26T10:00:05.000000",
          "message_id": "msg-002"
        }
      ]
    },
    {
      "conversation_id": "660e9400-f29b-41d4-b716-557755551111",
      "user_id": "2",
      "username": "bob",
      "created_at": "2025-04-26T11:00:00.000000",
      "updated_at": "2025-04-26T11:20:00.000000",
      "messages": [
        {
          "role": "user",
          "content": "Explain Python decorators",
          "timestamp": "2025-04-26T11:00:00.000000",
          "message_id": "msg-001"
        },
        {
          "role": "bot",
          "content": "Decorators in Python are functions that modify the behavior of other functions or classes...",
          "timestamp": "2025-04-26T11:00:10.000000",
          "message_id": "msg-002"
        }
      ]
    },
    {
      "conversation_id": "770e0500-g29b-41d4-c716-668866662222",
      "user_id": "1",
      "username": "alice",
      "created_at": "2025-04-26T14:00:00.000000",
      "updated_at": "2025-04-26T14:30:00.000000",
      "messages": [
        {
          "role": "user",
          "content": "How do I learn web development?",
          "timestamp": "2025-04-26T14:00:00.000000",
          "message_id": "msg-001"
        },
        {
          "role": "bot",
          "content": "To learn web development, start with: 1) HTML & CSS basics 2) JavaScript 3) Frontend framework (React/Vue) 4) Backend (Node.js/Python) 5) Databases",
          "timestamp": "2025-04-26T14:00:15.000000",
          "message_id": "msg-002"
        },
        {
          "role": "user",
          "content": "Which frontend framework should I choose?",
          "timestamp": "2025-04-26T14:05:00.000000",
          "message_id": "msg-003"
        },
        {
          "role": "bot",
          "content": "Popular choices: React (most popular, big ecosystem), Vue (easier to learn), Angular (enterprise). Start with React or Vue!",
          "timestamp": "2025-04-26T14:05:20.000000",
          "message_id": "msg-004"
        }
      ]
    }
  ]
}


# Example 3: Large conversation with context
{
  "conversations": [
    {
      "conversation_id": "880f1600-h29b-41d4-d716-779977773333",
      "user_id": "3",
      "username": "charlie",
      "created_at": "2025-04-26T09:00:00.000000",
      "updated_at": "2025-04-26T09:45:00.000000",
      "messages": [
        {
          "role": "user",
          "content": "I want to build a Python web application",
          "timestamp": "2025-04-26T09:00:00.000000",
          "message_id": "msg-001"
        },
        {
          "role": "bot",
          "content": "Great! Python web development is awesome. Popular frameworks include Flask, Django, and FastAPI. What's your experience level?",
          "timestamp": "2025-04-26T09:00:10.000000",
          "message_id": "msg-002"
        },
        {
          "role": "user",
          "content": "I'm a beginner but I know Python basics",
          "timestamp": "2025-04-26T09:02:00.000000",
          "message_id": "msg-003"
        },
        {
          "role": "bot",
          "content": "Perfect! I recommend starting with Flask because it's lightweight and great for learning. Here's what you need to learn: 1) Flask routing 2) Templates (Jinja2) 3) Database models 4) Forms 5) User authentication",
          "timestamp": "2025-04-26T09:02:15.000000",
          "message_id": "msg-004"
        },
        {
          "role": "user",
          "content": "Can you explain routing?",
          "timestamp": "2025-04-26T09:05:00.000000",
          "message_id": "msg-005"
        },
        {
          "role": "bot",
          "content": "Routing maps URLs to functions. For example:\n@app.route('/hello')\ndef hello():\n    return 'Hello World!'\n\nThis creates a route at http://domain/hello that returns 'Hello World!'",
          "timestamp": "2025-04-26T09:05:20.000000",
          "message_id": "msg-006"
        },
        {
          "role": "user",
          "content": "What about dynamic routes?",
          "timestamp": "2025-04-26T09:10:00.000000",
          "message_id": "msg-007"
        },
        {
          "role": "bot",
          "content": "Dynamic routes use variables in the URL:\n@app.route('/user/<name>')\ndef greet_user(name):\n    return f'Hello {name}!'\n\nVisiting /user/alice returns 'Hello alice!'",
          "timestamp": "2025-04-26T09:10:15.000000",
          "message_id": "msg-008"
        },
        {
          "role": "user",
          "content": "This is really helpful! What should I do next?",
          "timestamp": "2025-04-26T09:15:00.000000",
          "message_id": "msg-009"
        },
        {
          "role": "bot",
          "content": "Next steps: 1) Build a simple Flask app with 2-3 routes 2) Add HTML templates 3) Learn about databases with SQLAlchemy 4) Add form handling. Practice by building a blog or todo app!",
          "timestamp": "2025-04-26T09:15:20.000000",
          "message_id": "msg-010"
        }
      ]
    }
  ]
}


# Structure Legend:
# ─────────────────────────────────────
# "conversation_id": Unique ID (UUID) for each conversation
# "user_id": The user's ID from the database
# "username": The user's username
# "created_at": When conversation started (ISO 8601 format)
# "updated_at": Last message timestamp (ISO 8601 format)
# "messages": Array of all messages in the conversation
#   "role": Either "user" or "bot"
#   "content": The actual message text
#   "timestamp": When the message was sent
#   "message_id": Unique ID for each message

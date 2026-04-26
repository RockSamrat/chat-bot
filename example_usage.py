"""
example_usage.py - Demonstrates how to use the conversation storage system.

This script shows practical examples of:
1. Creating and storing conversations
2. Retrieving conversations
3. Exporting conversations
4. Using with the Flask API
"""

# ─────────── Example 1: Direct API Usage ───────────
print("=" * 60)
print("EXAMPLE 1: Using Conversations Module Directly")
print("=" * 60)

from backend.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_user_conversations,
    get_conversation_context,
    export_conversation_to_file,
)

# Create a new conversation
user_id = "1"
username = "john_doe"
conversation = create_new_conversation(user_id, username)
conversation_id = conversation["conversation_id"]

print(f"\n✓ Created conversation: {conversation_id}")
print(f"  User: {username} (ID: {user_id})")

# Add messages to the conversation
print("\n→ Adding messages to conversation...")
add_message(conversation_id, "user", "What is Python?", user_id, username)
print("  • User message added: 'What is Python?'")

add_message(conversation_id, "bot",
            "Python is a powerful programming language...",
            user_id, username)
print("  • Bot response added")

add_message(conversation_id, "user", "Can you give me an example?", user_id, username)
print("  • User message added: 'Can you give me an example?'")

add_message(conversation_id, "bot",
            "Sure! Here's a simple example: print('Hello, World!')",
            user_id, username)
print("  • Bot response added")

# Retrieve and display the conversation
print("\n→ Retrieving stored conversation...")
stored_conversation = get_conversation(conversation_id)
if stored_conversation:
    print(f"✓ Conversation retrieved successfully!")
    print(f"  Messages count: {len(stored_conversation['messages'])}")
    print(f"  Created at: {stored_conversation['created_at']}")
    print(f"  Updated at: {stored_conversation['updated_at']}")

# Get conversation context (useful for LLM)
print("\n→ Extracting conversation context for LLM...")
context = get_conversation_context(conversation_id, limit=3)
print("Context (last 3 messages):")
print(context)

# Get all conversations for this user
print("\n→ Retrieving all conversations for this user...")
user_conversations = get_user_conversations(user_id)
print(f"✓ Found {len(user_conversations)} conversation(s) for {username}")

# Export conversation to file
print("\n→ Exporting conversation to file...")
export_path = export_conversation_to_file(conversation_id)
if export_path:
    print(f"✓ Exported to: {export_path}")


# ─────────── Example 2: Flask API Usage ───────────
print("\n" + "=" * 60)
print("EXAMPLE 2: Using with Flask API (Tkinter Integration)")
print("=" * 60)

import uuid
import requests

# Sample API credentials (you'll get these from login)
API_URL = "http://localhost:5000"
TOKEN = "your-jwt-token-here"  # Replace with actual token from login

# Sample function to integrate into your GUI
def send_chat_message_with_storage(question: str, conversation_id: str = None) -> dict:
    """
    Send a chat message and automatically store it in conversations.

    This is how you would integrate it into chat-bot-gui.py
    """
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {
        "question": question,
        "conversation_id": conversation_id
    }

    try:
        response = requests.post(
            f"{API_URL}/api/chat",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Message sent successfully")
            print(f"  Question: {question}")
            print(f"  Response: {data['response'][:100]}...")
            print(f"  Conversation ID: {data['conversation_id']}")
            return data
        else:
            print(f"✗ Error: {response.json().get('error')}")
            return None

    except Exception as e:
        print(f"✗ Failed to connect to server: {e}")
        return None


print("\nSample function (send_chat_message_with_storage) is ready to use.")
print("Usage in your GUI:")
print("""
    # In your send() function:
    current_conversation_id = str(uuid.uuid4())

    def send(event=None):
        msg = input_box.get().strip()
        if not msg:
            return

        result = send_chat_message_with_storage(msg, current_conversation_id)
        if result:
            add_bubble("Bot", result["response"], is_user=False)
""")


# ─────────── Example 3: Viewing Stored Conversations ───────────
print("\n" + "=" * 60)
print("EXAMPLE 3: Viewing All Stored Conversations")
print("=" * 60)

from backend.conversations import load_conversations
import json

data = load_conversations()
all_conversations = data.get("conversations", [])

print(f"\n✓ Total conversations stored: {len(all_conversations)}")
print("\nConversation Summary:")
print("-" * 60)

for i, conv in enumerate(all_conversations, 1):
    print(f"\n{i}. {conv['username']}")
    print(f"   ID: {conv['conversation_id']}")
    print(f"   Messages: {len(conv['messages'])}")
    print(f"   Created: {conv['created_at']}")

    # Show first and last message
    if conv['messages']:
        first_msg = conv['messages'][0]
        print(f"   First message: {first_msg['content'][:50]}...")


# ─────────── Example 4: Custom Analysis ───────────
print("\n" + "=" * 60)
print("EXAMPLE 4: Analyzing Conversation Data")
print("=" * 60)

if all_conversations:
    # Get statistics
    total_messages = sum(len(c['messages']) for c in all_conversations)
    avg_messages = total_messages / len(all_conversations) if all_conversations else 0

    print(f"\n Conversation Statistics:")
    print(f"   Total conversations: {len(all_conversations)}")
    print(f"   Total messages: {total_messages}")
    print(f"   Average messages per conversation: {avg_messages:.1f}")

    # User breakdown
    users = {}
    for conv in all_conversations:
        username = conv['username']
        users[username] = users.get(username, 0) + 1

    print(f"\n👥 Messages by user:")
    for username, count in sorted(users.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {username}: {count} conversation(s)")


print("\n" + "=" * 60)
print("All examples completed! ✓")
print("=" * 60)

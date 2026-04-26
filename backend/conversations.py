"""
conversations.py - Handle conversation storage in JSON format.

This module provides functions to:
- Load existing conversations from a JSON file
- Save new messages to a conversation
- Create conversations with proper structure
- Handle file creation and error handling
"""

import json
import os
from datetime import datetime
from uuid import uuid4


# Configuration
CONVERSATIONS_DIR = "data/conversations"
CONVERSATIONS_FILE = os.path.join(CONVERSATIONS_DIR, "conversations.json")


def ensure_directory_exists():
    """Create the conversations directory if it doesn't exist."""
    if not os.path.exists(CONVERSATIONS_DIR):
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)


def ensure_file_exists():
    """Create the conversations.json file if it doesn't exist."""
    ensure_directory_exists()
    if not os.path.exists(CONVERSATIONS_FILE):
        initial_data = {"conversations": []}
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=2)


def load_conversations():
    """
    Load all conversations from the JSON file.

    Returns:
        dict: A dictionary with a "conversations" key containing a list of all conversations.

    Raises:
        JSONDecodeError: If the JSON file is corrupted.
    """
    ensure_file_exists()
    try:
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(f"[ERROR] Corrupted JSON file: {CONVERSATIONS_FILE}")
        # Return empty structure instead of crashing
        return {"conversations": []}
    except Exception as e:
        print(f"[ERROR] Failed to load conversations: {e}")
        return {"conversations": []}


def save_conversations(data):
    """
    Save conversations back to the JSON file.

    Args:
        data (dict): The conversations data to save.

    Returns:
        bool: True if successful, False otherwise.
    """
    ensure_directory_exists()
    try:
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save conversations: {e}")
        return False


def create_new_conversation(user_id, username):
    """
    Create a new conversation entry.

    Args:
        user_id (str): The ID of the user.
        username (str): The username of the user.

    Returns:
        dict: A new conversation object with metadata.
    """
    return {
        "conversation_id": str(uuid4()),
        "user_id": user_id,
        "username": username,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "messages": []
    }


def add_message(conversation_id, role, content, user_id, username):
    """
    Add a new message to a conversation.

    Args:
        conversation_id (str): The ID of the conversation to add the message to.
        role (str): Either "user" or "bot".
        content (str): The message content.
        user_id (str): The user's ID.
        username (str): The user's username.

    Returns:
        bool: True if the message was added successfully, False otherwise.
    """
    if role not in ["user", "bot"]:
        print(f"[ERROR] Invalid role: {role}")
        return False

    try:
        data = load_conversations()
        conversations = data.get("conversations", [])

        # Find the conversation
        conversation = None
        for conv in conversations:
            if conv["conversation_id"] == conversation_id:
                conversation = conv
                break

        # If conversation doesn't exist, create it
        if conversation is None:
            conversation = create_new_conversation(user_id, username)
            conversations.append(conversation)

        # Add the message
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "message_id": str(uuid4())
        }
        conversation["messages"].append(message)
        conversation["updated_at"] = datetime.now().isoformat()

        # Save back to file
        data["conversations"] = conversations
        return save_conversations(data)

    except Exception as e:
        print(f"[ERROR] Failed to add message: {e}")
        return False


def get_conversation(conversation_id):
    """
    Retrieve a specific conversation by ID.

    Args:
        conversation_id (str): The ID of the conversation to retrieve.

    Returns:
        dict or None: The conversation object if found, None otherwise.
    """
    try:
        data = load_conversations()
        conversations = data.get("conversations", [])

        for conv in conversations:
            if conv["conversation_id"] == conversation_id:
                return conv
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get conversation: {e}")
        return None


def get_user_conversations(user_id):
    """
    Get all conversations for a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of conversation objects for the user.
    """
    try:
        data = load_conversations()
        conversations = data.get("conversations", [])
        user_conversations = [
            conv for conv in conversations if conv["user_id"] == user_id
        ]
        return user_conversations
    except Exception as e:
        print(f"[ERROR] Failed to get user conversations: {e}")
        return []


def get_conversation_context(conversation_id, limit=5):
    """
    Get recent messages from a conversation for context.

    Args:
        conversation_id (str): The ID of the conversation.
        limit (int): Maximum number of previous messages to retrieve for context.

    Returns:
        str: Formatted conversation history as a string.
    """
    conversation = get_conversation(conversation_id)
    if not conversation:
        return ""

    messages = conversation.get("messages", [])

    # Get the last 'limit' messages (excluding the most recent one)
    context_messages = messages[:-1] if messages else []
    context_messages = context_messages[-limit:]

    # Format as a readable context string
    context = ""
    for msg in context_messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        context += f"\n{role}: {content}"

    return context.strip()


def export_conversation_to_file(conversation_id, output_filename=None):
    """
    Export a conversation to a separate JSON file.

    Args:
        conversation_id (str): The ID of the conversation to export.
        output_filename (str, optional): Custom filename. If None, uses conversation_id.

    Returns:
        str or None: The path to the exported file if successful, None otherwise.
    """
    conversation = get_conversation(conversation_id)
    if not conversation:
        print(f"[ERROR] Conversation not found: {conversation_id}")
        return None

    filename = output_filename or f"{conversation_id}.json"
    filepath = os.path.join(CONVERSATIONS_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
        return filepath
    except Exception as e:
        print(f"[ERROR] Failed to export conversation: {e}")
        return None

#!/usr/bin/env python3
"""
test_conversation_saving.py - Debug conversation saving issues

Run this to test if conversation saving is working properly.
"""

import os
import sys
import json
import requests
from datetime import datetime

# Ensure we're in the right directory
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

print("=" * 70)
print("CONVERSATION STORAGE DEBUGGING")
print("=" * 70)

# 1. Check directory structures
print("\n1. Checking directory structure...")
print(f"   Current working directory: {os.getcwd()}")

if os.path.exists("data/conversations"):
    print(f"   ✓ data/conversations/ exists")
else:
    print(f"   ✗ data/conversations/ does NOT exist (will be created)")

# 2. Test module imports
print("\n2. Testing module imports...")
try:
    from backend.conversations import (
        ensure_directory_exists,
        ensure_file_exists,
        add_message,
        get_conversation,
        load_conversations,
    )
    print("   ✓ Conversations module imported successfully")
except Exception as e:
    print(f"   ✗ ERROR importing module: {e}")
    sys.exit(1)

# 3. Test file/directory creation
print("\n3. Testing file/directory creation...")
try:
    ensure_directory_exists()
    ensure_file_exists()

    conv_file = os.path.join(os.getcwd(), "data/conversations/conversations.json")
    if os.path.exists(conv_file):
        print(f"   ✓ Conversations file created: {conv_file}")
        with open(conv_file, "r") as f:
            data = json.load(f)
        print(f"   ✓ File is valid JSON with {len(data.get('conversations', []))} conversation(s)")
    else:
        print(f"   ✗ Conversations file NOT created")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# 4. Test conversation operations
print("\n4. Testing conversation operations...")
try:
    # Add test conversation
    test_conv_id = "test-debug-" + datetime.now().strftime("%Y%m%d%H%M%S")

    # Note: This doesn't create a new conversation in the file,
    # but adds a message to it
    result = add_message(
        test_conv_id,
        "user",
        "Debug test message",
        "test_user",
        "test_username"
    )

    if result:
        print("   ✓ Message added successfully")

        # Try to load it back
        conv = get_conversation(test_conv_id)
        if conv:
            print(f"   ✓ Conversation retrieved: {len(conv['messages'])} message(s)")
        else:
            print(f"   ✗ Conversation NOT found after adding")
    else:
        print("   ✗ Failed to add message")

except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

# 5. Show file contents
print("\n5. Current conversations.json content:")
print("-" * 70)
try:
    with open("data/conversations/conversations.json", "r") as f:
        data = json.load(f)
    # Pretty print with indentation
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"ERROR reading file: {e}")

# 6. API Testing Instructions
print("\n" + "=" * 70)
print("6. HOW TO TEST WITH FLASK SERVER:")
print("=" * 70)
print("""
Step 1: Start the Flask server in one terminal:
    python -m backend.server

Step 2: In another terminal, register/login to get a token:
    curl -X POST http://localhost:5000/api/auth/register \\
      -H "Content-Type: application/json" \\
      -d '{"username":"testuser","password":"password123"}'

    Save the token from the response.

Step 3: Send a chat message:
    curl -X POST http://localhost:5000/api/chat \\
      -H "Authorization: Bearer YOUR_TOKEN_HERE" \\
      -H "Content-Type: application/json" \\
      -d '{"question":"Hello, what is Python?"}'

Step 4: Check the conversations.json file:
    cat data/conversations/conversations.json

Step 5: Look for these debug messages in the Flask console:
    [chat] Creating new conversation for user testuser
    [chat] User message saved: True
    [chat] Bot message saved: True
    [chat] Response sent for conversation ...
""")

print("\n" + "=" * 70)
print("DEBUGGING CHECKLIST:")
print("=" * 70)
print("""
If conversations are NOT being saved:

□ Check that data/conversations/conversations.json exists
□ Check Flask console for [chat] debug messages
□ Verify the /api/chat route is being called
□ Check for any [chat] ERROR messages
□ Make sure you're using a valid JWT token
□ Verify Ollama is running and available
□ Check file permissions on data/conversations/ directory
□ Try running this test script first: python test_conversation_saving.py
""")

print("\n✓ Debug script completed!")

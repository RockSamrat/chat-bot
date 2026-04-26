"""
server.py - Flask backend.

Routes
------
POST /api/auth/register  create account
POST /api/auth/login     obtain JWT
GET  /api/auth/me        verify token & return profile   [protected]
POST /api/chat           proxy a chat turn to Ollama     [protected]
"""
"""

os → system settings
sys → runtime control
Flask → web server
request → incoming data
jsonify → outgoing response
g → store user data per request
CORS → allow frontend requests
dotenv → load .env config

"""
import os #Read environment variables and interact with the system
import sys #Logging to stderr, exiting, handling runtime info
from flask  import Flask, request, jsonify, g 
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ---------- Import project modules ----------
from backend.db import run_migrations
from backend.auth_model import UserModel
from backend.auth_middleware import create_token, require_auth
from backend.conversations import (
    add_message,
    get_user_conversations,
    get_conversation_context,
    create_new_conversation,
    save_conversations,
    load_conversations,
)

# ---------- Ollama / LangChain chain ----------
# Import lazily so the server can start even when Ollama is offline
try:
    from backend.main import chain as ollama_chain
    OLLAMA_AVAILABLE = True
except Exception as _e:
    ollama_chain = None
    OLLAMA_AVAILABLE = False
    print(f"[server] Warning: Ollama chain unavailable – {_e}", file=sys.stderr)

# ---------- App ----------
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------- Input validation helpers ----------
def _require_json_fields(required: list[str]):
    data = request.get_json(silent=True) or {}
    missing = [f for f in required if not data.get(f)]
    return data, missing


# ── Auth routes ──────────────────────────────────────────────

@app.post("/api/auth/register")
def register():
    data, missing = _require_json_fields(["username", "password"])
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    username: str = data["username"].strip()
    password: str = data["password"]

    # Basic validation
    if len(username) < 3 or len(username) > 50:
        return jsonify({"error": "Username must be 3–50 characters."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400
    if not username.replace("_", "").replace("-", "").isalnum():
        return jsonify({"error": "Username may only contain letters, numbers, - and _."}), 400

    try:
        user = UserModel.create_user(username, password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    token = create_token(str(user["id"]), user["username"])
    return jsonify({"token": token, "username": user["username"]}), 201


@app.post("/api/auth/login")
def login():
    data, missing = _require_json_fields(["username", "password"])
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    username: str = data["username"].strip()
    password: str = data["password"]

    user = UserModel.get_user_by_username(username)
    if not user or not UserModel.verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid username or password."}), 401

    token = create_token(str(user["id"]), user["username"])
    return jsonify({"token": token, "username": user["username"]}), 200


@app.get("/api/auth/me")
@require_auth
def me():
    return jsonify({"id": g.user["sub"], "username": g.user["username"]}), 200


# ── Chat route (protected) ────────────────────────────────────

@app.post("/api/chat")
@require_auth
def chat():
    data, missing = _require_json_fields(["question"])
    if missing:
        return jsonify({"error": "Missing 'question' field."}), 400

    question: str = data["question"].strip()
    conversation_id: str = data.get("conversation_id", "").strip()

    if not OLLAMA_AVAILABLE or ollama_chain is None:
        return jsonify({"error": "AI backend (Ollama) is not available."}), 503

    # Create a new conversation if one isn't provided
    if not conversation_id:
        new_conversation = create_new_conversation(g.user["sub"], g.user["username"])
        conversation_id = new_conversation["conversation_id"]
        # Save the new conversation to file
        all_data = load_conversations()
        all_data["conversations"].append(new_conversation)
        save_conversations(all_data)

    # Get conversation context if conversation_id is provided
    context: str = ""
    if conversation_id:
        context = get_conversation_context(conversation_id)

    try:
        # Save user message to conversation
        if conversation_id:
            add_message(conversation_id, "user", question, g.user["sub"], g.user["username"])

        # Get bot response
        full_response = ""
        for chunk in ollama_chain.stream({"context": context, "question": question}):
            full_response += chunk

        # Save bot response to conversation
        if conversation_id:
            add_message(conversation_id, "bot", full_response, g.user["sub"], g.user["username"])

        return jsonify({"response": full_response, "conversation_id": conversation_id}), 200
    except ConnectionError:
        return jsonify({"error": "Could not connect to Ollama. Is it running?"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Entry point ----------

if __name__ == "__main__":
    run_migrations()
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print(f"[server] Starting on http://localhost:{port}  debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
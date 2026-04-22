"""
server.py - Flask backend.

Routes
------
POST /api/auth/register  – create account
POST /api/auth/login     – obtain JWT
GET  /api/auth/me        – verify token & return profile   [protected]
POST /api/chat           – proxy a chat turn to Ollama     [protected]
"""

import os
import sys
from flask  import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ---------- Import project modules ----------
from backend.db import run_migrations
from backend.auth_model import UserModel
from backend.auth_middleware import create_token, require_auth

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
    context: str = data.get("context", "")

    if not OLLAMA_AVAILABLE or ollama_chain is None:
        return jsonify({"error": "AI backend (Ollama) is not available."}), 503

    try:
        full_response = ""
        for chunk in ollama_chain.stream({"context": context, "question": question}):
            full_response += chunk
        return jsonify({"response": full_response}), 200
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
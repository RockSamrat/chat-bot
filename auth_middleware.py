"""
auth_middleware.py - JWT token creation, verification, and Flask auth middleware.
"""

import os
import functools
import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify, g
from dotenv import load_dotenv

load_dotenv()

# Secret key – set JWT_SECRET in .env for production, falls back to a default for dev
JWT_SECRET: str = os.getenv("JWT_SECRET", "changeme-use-a-long-random-secret")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24


def create_token(user_id: str, username: str) -> str:
    """Create a signed JWT for the given user."""
    payload = {
        "sub": user_id,
        "username": username,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure.
    """
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def _extract_bearer(auth_header: str | None) -> str | None:
    """Pull token out of 'Bearer <token>' header."""
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ", 1)[1]


def require_auth(f):
    """
    Flask route decorator that enforces JWT authentication.
    Populates flask.g.user with the decoded token payload.
    """
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_bearer(request.headers.get("Authorization"))
        if not token:
            return jsonify({"error": "Missing or invalid Authorization header."}), 401
        try:
            g.user = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token."}), 401
        return f(*args, **kwargs)
    return decorated
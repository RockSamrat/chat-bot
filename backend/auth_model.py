"""
auth_model.py - User model with password hashing and DB operations.
"""

import bcrypt
import psycopg2.extras
from backend.db import get_conn, put_conn


class UserModel:
    @staticmethod
    def hash_password(plain: str) -> str:
        """Return bcrypt hash of the plain-text password."""
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Check plain password against stored hash."""
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    @staticmethod
    def create_user(username: str, password: str) -> dict:
        """
        Insert a new user. Returns the created user dict.
        Raises ValueError on duplicate username.
        """
        password_hash = UserModel.hash_password(password)
        conn = get_conn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO users (username, password_hash)
                    VALUES (%s, %s)
                    RETURNING id, username, created_at
                    """,
                    (username, password_hash),
                )
                user = dict(cur.fetchone())
            conn.commit()
            return user
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("Username already taken.")
        except Exception:
            conn.rollback()
            raise
        finally:
            put_conn(conn)

    @staticmethod
    def get_user_by_username(username: str) -> dict | None:
        """Fetch user row by username, or None if not found."""
        conn = get_conn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, username, password_hash FROM users WHERE username = %s",
                    (username,),
                )
                row = cur.fetchone()
                return dict(row) if row else None
        finally:
            put_conn(conn)
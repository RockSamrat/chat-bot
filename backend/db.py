"""
db.py - Database connection pool and schema migration for Neon PostgreSQL.
"""

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL not set in .env")

# Connection pool (min 1, max 10 connections)
_pool: pool.SimpleConnectionPool | None = None  #_pool is a global variable (shared across app) //Connections are reused → fast + efficient


def get_pool() -> pool.SimpleConnectionPool:
    global _pool
    if _pool is None:
        _pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)
    return _pool


def get_conn():
    """Borrow a connection from the pool."""
    return get_pool().getconn()


def put_conn(conn):
    """Return a connection to the pool."""
    get_pool().putconn(conn)


def run_migrations():
    """Create tables and indexes if they don't exist."""
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        sql = f.read()

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print("[db] Migrations applied successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[db] Migration error: {e}")
        raise
    finally:
        put_conn(conn)


if __name__ == "__main__":
    run_migrations()
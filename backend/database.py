## SQLite database initialisation and helpers

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Read from .env / environment; fall back to a local file
DB_PATH = os.getenv("DB_PATH", str(Path(__file__).parent.parent / "data" / "hirelytics.db"))


def get_connection() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    """Context manager that yields a connection and auto-commits / rolls back."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist yet."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                name     TEXT    NOT NULL,
                email    TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    print(f"[DB] Initialised at {DB_PATH}")

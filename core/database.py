import sqlite3
import os
import hashlib
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "quant_algo.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = "quant_algo_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def init_db():
    """Create tables if they don't exist and seed default admin."""
    conn = get_connection()
    cursor = conn.cursor()

    # Admins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Auth tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_tokens (
            token TEXT PRIMARY KEY,
            admin_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (admin_id) REFERENCES admins (id) ON DELETE CASCADE
        )
    """)

    # Check if default admin exists; if not, create one
    cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
    if not cursor.fetchone():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO admins (username, email, password_hash, role, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "admin",
            "admin@quantalgo.com",
            hash_password("admin123"),
            "superadmin",
            1,
            now,
            now
        ))
        print("[DB] Default admin created: username='admin', password='admin123'")

    conn.commit()
    conn.close()

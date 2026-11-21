import uuid
from datetime import datetime
from core.database import get_connection, hash_password


def login_admin(username_or_email: str, password: str):
    """
    Authenticate admin with username or email + password.
    Returns auth token and admin profile.
    """
    if not username_or_email or not password:
        raise ValueError("Username/Email and Password are required")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM admins
        WHERE (username = ? OR email = ?) AND is_active = 1
    """, (username_or_email, username_or_email))

    admin = cursor.fetchone()

    if not admin:
        conn.close()
        raise ValueError("Invalid username/email or password")

    # Verify password hash
    if admin["password_hash"] != hash_password(password):
        conn.close()
        raise ValueError("Invalid username/email or password")

    # Generate session token
    token = f"tok_{uuid.uuid4().hex}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO auth_tokens (token, admin_id, created_at)
        VALUES (?, ?, ?)
    """, (token, admin["id"], now))

    conn.commit()
    conn.close()

    return {
        "token": token,
        "admin": {
            "id": admin["id"],
            "username": admin["username"],
            "email": admin["email"],
            "role": admin["role"],
            "created_at": admin["created_at"]
        }
    }


def verify_token(token: str):
    """
    Validate an auth token and return the associated admin.
    """
    if not token:
        raise ValueError("Token is required")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, a.username, a.email, a.role, a.is_active, a.created_at
        FROM auth_tokens t
        JOIN admins a ON t.admin_id = a.id
        WHERE t.token = ? AND a.is_active = 1
    """, (token,))

    admin = cursor.fetchone()
    conn.close()

    if not admin:
        raise ValueError("Invalid or expired session token")

    return dict(admin)


def logout_admin(token: str):
    """
    Invalidate an auth token.
    """
    if not token:
        return True

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auth_tokens WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True

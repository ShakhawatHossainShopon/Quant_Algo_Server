from datetime import datetime
from core.database import get_connection, hash_password


def list_all_admins():
    """Retrieve all admins without exposing password hashes."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM admins
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_admin_by_id(admin_id: int):
    """Retrieve a single admin by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM admins
        WHERE id = ?
    """, (admin_id,))

    admin = cursor.fetchone()
    conn.close()

    if not admin:
        raise ValueError(f"Admin with ID {admin_id} not found")

    return dict(admin)


def create_new_admin(username: str, email: str, password: str, role: str = "admin"):
    """Create a new admin user."""
    if not username or not email or not password:
        raise ValueError("Username, Email, and Password are all required")

    conn = get_connection()
    cursor = conn.cursor()

    # Check for existing username or email
    cursor.execute("SELECT id FROM admins WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise ValueError(f"Username '{username}' already exists")

    cursor.execute("SELECT id FROM admins WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        raise ValueError(f"Email '{email}' already registered")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pwd_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO admins (username, email, password_hash, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, 1, ?, ?)
    """, (username, email, pwd_hash, role, now, now))

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_admin_by_id(new_id)


def update_existing_admin(admin_id: int, data: dict):
    """Update admin fields (username, email, password, role, is_active)."""
    admin = get_admin_by_id(admin_id)  # Throws ValueError if not found

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updates = []
    params = []

    if "username" in data and data["username"]:
        cursor.execute("SELECT id FROM admins WHERE username = ? AND id != ?", (data["username"], admin_id))
        if cursor.fetchone():
            conn.close()
            raise ValueError(f"Username '{data['username']}' is already in use")
        updates.append("username = ?")
        params.append(data["username"])

    if "email" in data and data["email"]:
        cursor.execute("SELECT id FROM admins WHERE email = ? AND id != ?", (data["email"], admin_id))
        if cursor.fetchone():
            conn.close()
            raise ValueError(f"Email '{data['email']}' is already in use")
        updates.append("email = ?")
        params.append(data["email"])

    if "password" in data and data["password"]:
        updates.append("password_hash = ?")
        params.append(hash_password(data["password"]))

    if "role" in data and data["role"]:
        updates.append("role = ?")
        params.append(data["role"])

    if "is_active" in data:
        updates.append("is_active = ?")
        params.append(int(data["is_active"]))

    if not updates:
        conn.close()
        return admin

    updates.append("updated_at = ?")
    params.append(now)
    params.append(admin_id)

    query = f"UPDATE admins SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

    return get_admin_by_id(admin_id)


def delete_admin_by_id(admin_id: int):
    """Delete an admin by ID (prevents deleting last superadmin)."""
    admin = get_admin_by_id(admin_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM admins WHERE role = 'superadmin' AND is_active = 1")
    superadmin_count = cursor.fetchone()["count"]

    if admin["role"] == "superadmin" and superadmin_count <= 1:
        conn.close()
        raise ValueError("Cannot delete the only remaining superadmin")

    cursor.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
    cursor.execute("DELETE FROM auth_tokens WHERE admin_id = ?", (admin_id,))

    conn.commit()
    conn.close()

    return {"deleted": True, "id": admin_id, "username": admin["username"]}

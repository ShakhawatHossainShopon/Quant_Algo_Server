from services.auth_service import login_admin, verify_token, logout_admin


def login_controller(payload):
    """
    POST /api/auth/login
    Payload: { "username": "admin", "password": "admin123" }
    """
    try:
        if not payload:
            return {"success": False, "message": "Request body cannot be empty"}, 400

        username_or_email = payload.get("username") or payload.get("email")
        password = payload.get("password")

        result = login_admin(username_or_email, password)
        return {
            "success": True,
            "message": "Login successful",
            "data": result
        }, 200

    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 401
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def me_controller(payload=None):
    """
    POST /api/auth/me
    Payload: { "token": "tok_..." }
    """
    try:
        token = None
        if payload and isinstance(payload, dict):
            token = payload.get("token")

        if not token:
            return {"success": False, "message": "Auth token is required"}, 401

        admin = verify_token(token)
        return {
            "success": True,
            "data": admin
        }, 200

    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 401
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def logout_controller(payload=None):
    """
    POST /api/auth/logout
    Payload: { "token": "tok_..." }
    """
    try:
        token = payload.get("token") if payload else None
        logout_admin(token)
        return {
            "success": True,
            "message": "Logged out successfully"
        }, 200

    except Exception as e:
        return {"success": False, "message": str(e)}, 500

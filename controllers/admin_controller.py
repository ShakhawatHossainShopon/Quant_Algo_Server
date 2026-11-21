from services.admin_service import (
    list_all_admins,
    get_admin_by_id,
    create_new_admin,
    update_existing_admin,
    delete_admin_by_id
)


def list_admins_controller():
    """
    GET /api/admin/list
    """
    try:
        admins = list_all_admins()
        return {
            "success": True,
            "count": len(admins),
            "data": admins
        }, 200
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def get_admin_controller(payload=None):
    """
    POST /api/admin/get
    Payload: { "id": 1 }
    """
    try:
        if not payload or "id" not in payload:
            return {"success": False, "message": "Admin 'id' is required"}, 400

        admin = get_admin_by_id(int(payload["id"]))
        return {
            "success": True,
            "data": admin
        }, 200
    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 404
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def create_admin_controller(payload):
    """
    POST /api/admin/create
    Payload: {
        "username": "trader1",
        "email": "trader1@quantalgo.com",
        "password": "secretpassword",
        "role": "admin"
    }
    """
    try:
        if not payload:
            return {"success": False, "message": "Payload is required"}, 400

        username = payload.get("username")
        email = payload.get("email")
        password = payload.get("password")
        role = payload.get("role", "admin")

        new_admin = create_new_admin(username, email, password, role)
        return {
            "success": True,
            "message": "Admin created successfully",
            "data": new_admin
        }, 201
    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 400
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def update_admin_controller(payload):
    """
    POST /api/admin/update
    Payload: {
        "id": 2,
        "email": "newemail@quantalgo.com",
        "role": "manager"
    }
    """
    try:
        if not payload or "id" not in payload:
            return {"success": False, "message": "Admin 'id' is required for update"}, 400

        admin_id = int(payload["id"])
        updated = update_existing_admin(admin_id, payload)
        return {
            "success": True,
            "message": "Admin updated successfully",
            "data": updated
        }, 200
    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 400
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def delete_admin_controller(payload):
    """
    POST /api/admin/delete
    Payload: { "id": 2 }
    """
    try:
        if not payload or "id" not in payload:
            return {"success": False, "message": "Admin 'id' is required for deletion"}, 400

        admin_id = int(payload["id"])
        result = delete_admin_by_id(admin_id)
        return {
            "success": True,
            "message": "Admin deleted successfully",
            "data": result
        }, 200
    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 400
    except Exception as e:
        return {"success": False, "message": str(e)}, 500

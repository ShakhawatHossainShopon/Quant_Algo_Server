from services.demo_service import get_demo_data, process_demo_order


def get_demo_controller():
    """
    Handles GET requests for demo data.
    """
    try:
        data = get_demo_data()
        return {
            "success": True,
            "data": data
        }, 200

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500


def post_demo_controller(payload):
    """
    Handles POST requests with JSON payload.
    """
    try:
        if not payload:
            payload = {}

        result = process_demo_order(payload)
        return {
            "success": True,
            "data": result
        }, 200

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500

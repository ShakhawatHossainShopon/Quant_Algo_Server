from services.mt5_service import (
    get_account_details,
    get_open_positions,
    create_position,
    close_position_by_ticket,
    get_available_symbols
)


def get_symbols_controller():
    """
    GET /api/mt5/symbols
    Returns list of tradeable assets/symbols.
    """
    try:
        symbols = get_available_symbols()
        return {
            "success": True,
            "count": len(symbols),
            "data": symbols
        }, 200
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500


def get_account_controller():
    """
    GET /api/mt5/account
    Returns account balance, equity, leverage, etc.
    """
    try:
        data = get_account_details()
        return {
            "success": True,
            "data": data
        }, 200
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500


def get_positions_controller():
    """
    GET /api/mt5/positions
    Returns currently open and active positions.
    """
    try:
        positions = get_open_positions()
        return {
            "success": True,
            "count": len(positions),
            "data": positions
        }, 200
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500


def create_position_controller(payload):
    """
    POST /api/mt5/position/create
    Payload: {
        "symbol": "EURUSD",
        "action": "BUY", // or "SELL"
        "volume": 0.01,
        "sl": 0.0,
        "tp": 0.0,
        "comment": "My trade"
    }
    """
    try:
        if not payload:
            return {"success": False, "message": "Payload is required"}, 400

        symbol = payload.get("symbol")
        order_type = payload.get("action") or payload.get("type") or payload.get("order_type")
        lots = payload.get("volume") or payload.get("lots")
        sl = float(payload.get("sl", 0.0))
        tp = float(payload.get("tp", 0.0))
        comment = payload.get("comment", "QuantAlgo Trade")

        if not symbol or not order_type or not lots:
            return {
                "success": False,
                "message": "Missing required fields: symbol, action (BUY/SELL), and volume are required"
            }, 400

        result = create_position(
            symbol=symbol,
            order_type=order_type,
            lots=float(lots),
            sl=sl,
            tp=tp,
            comment=comment
        )

        return {
            "success": True,
            "message": f"Position {order_type.upper()} {lots} {symbol} opened successfully",
            "data": result
        }, 201

    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 400
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


def close_position_controller(payload):
    """
    POST /api/mt5/position/close
    Payload: { "ticket": 12345678 }
    """
    try:
        if not payload or "ticket" not in payload:
            return {"success": False, "message": "Position 'ticket' ID is required"}, 400

        ticket = int(payload["ticket"])
        result = close_position_by_ticket(ticket)

        return {
            "success": True,
            "message": f"Position #{ticket} closed successfully",
            "data": result
        }, 200

    except ValueError as ve:
        return {"success": False, "message": str(ve)}, 404
    except Exception as e:
        return {"success": False, "message": str(e)}, 500

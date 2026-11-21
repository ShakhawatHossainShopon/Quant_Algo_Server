from datetime import datetime


def get_demo_data():
    """
    Demo service to fetch sample market/system data.
    Replace this with your business logic (e.g. MT5, DB, indicators).
    """
    return {
        "service": "demo_service",
        "status": "online",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sample_symbols": ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD"],
        "message": "Demo service executed successfully"
    }


def process_demo_order(payload):
    """
    Demo service to process incoming POST payload (e.g. order, signal).
    """
    symbol = payload.get("symbol", "EURUSD")
    action = payload.get("action", "BUY")
    volume = payload.get("volume", 0.01)

    return {
        "service": "demo_service",
        "order_status": "simulated_success",
        "symbol": symbol,
        "action": action,
        "volume": volume,
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

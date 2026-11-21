import time
from datetime import datetime
import MetaTrader5 as mt5


def _ensure_mt5_connected():
    """Initializes connection to the running MetaTrader 5 terminal."""
    try:
        term_info = mt5.terminal_info()
        if term_info is not None and getattr(term_info, "connected", False):
            return True
    except Exception:
        pass

    if not mt5.initialize(timeout=3000):
        err = mt5.last_error()
        raise RuntimeError(
            f"MT5 terminal initialization failed: {err}. "
            "Please ensure MetaTrader 5 desktop terminal is open and logged into your trading account."
        )


def get_available_symbols():
    """
    Fetches list of available symbols from MetaTrader 5 terminal.
    Falls back to a curated list of standard assets if terminal is offline.
    """
    default_symbols = [
        {"symbol": "EURUSD", "category": "Forex Majors", "description": "Euro vs US Dollar"},
        {"symbol": "GBPUSD", "category": "Forex Majors", "description": "British Pound vs US Dollar"},
        {"symbol": "USDJPY", "category": "Forex Majors", "description": "US Dollar vs Japanese Yen"},
        {"symbol": "USDCHF", "category": "Forex Majors", "description": "US Dollar vs Swiss Franc"},
        {"symbol": "AUDUSD", "category": "Forex Majors", "description": "Australian Dollar vs US Dollar"},
        {"symbol": "USDCAD", "category": "Forex Majors", "description": "US Dollar vs Canadian Dollar"},
        {"symbol": "NZDUSD", "category": "Forex Majors", "description": "NZ Dollar vs US Dollar"},
        {"symbol": "EURJPY", "category": "Forex Crosses", "description": "Euro vs Japanese Yen"},
        {"symbol": "GBPJPY", "category": "Forex Crosses", "description": "British Pound vs Japanese Yen"},
        {"symbol": "EURGBP", "category": "Forex Crosses", "description": "Euro vs British Pound"},
        {"symbol": "AUDJPY", "category": "Forex Crosses", "description": "Australian Dollar vs Japanese Yen"},
        {"symbol": "XAUUSD", "category": "Metals & Energy", "description": "Gold vs US Dollar"},
        {"symbol": "XAGUSD", "category": "Metals & Energy", "description": "Silver vs US Dollar"},
        {"symbol": "USOIL", "category": "Metals & Energy", "description": "Crude Oil WTI"},
        {"symbol": "BTCUSD", "category": "Crypto", "description": "Bitcoin vs US Dollar"},
        {"symbol": "ETHUSD", "category": "Crypto", "description": "Ethereum vs US Dollar"},
        {"symbol": "US500", "category": "Indices", "description": "S&P 500 Index"},
        {"symbol": "US30", "category": "Indices", "description": "Dow Jones 30 Index"},
        {"symbol": "USTEC", "category": "Indices", "description": "Nasdaq 100 Index"},
    ]

    try:
        _ensure_mt5_connected()
        symbols = mt5.symbols_get()
        if symbols:
            res = []
            for s in symbols:
                if s.visible or len(res) < 100:
                    res.append({
                        "symbol": s.name,
                        "category": "Broker Symbol",
                        "description": s.description or s.name
                    })
            if res:
                return res
    except Exception:
        pass

    return default_symbols


def get_account_details():
    """
    Fetches real-time account summary (balance, equity, margin, leverage, etc.)
    """
    _ensure_mt5_connected()
    acc = mt5.account_info()
    if acc is None:
        raise RuntimeError(f"Failed to fetch account info: {mt5.last_error()}")

    data = acc._asdict()
    return {
        "login": data.get("login"),
        "server": data.get("server"),
        "name": data.get("name"),
        "currency": data.get("currency"),
        "leverage": data.get("leverage"),
        "balance": round(float(data.get("balance", 0.0)), 2),
        "equity": round(float(data.get("equity", 0.0)), 2),
        "profit": round(float(data.get("profit", 0.0)), 2),
        "margin": round(float(data.get("margin", 0.0)), 2),
        "margin_free": round(float(data.get("margin_free", 0.0)), 2),
        "margin_level": round(float(data.get("margin_level", 0.0)), 2) if data.get("margin_level") else 0.0,
        "trade_mode": "Demo" if data.get("trade_mode") == 0 else "Real"
    }


def get_open_positions():
    """
    Fetches all currently open and running trading positions.
    """
    _ensure_mt5_connected()
    positions = mt5.positions_get()
    if positions is None:
        return []

    result = []
    for pos in positions:
        p = pos._asdict()
        pos_type = "BUY" if p.get("type") == mt5.POSITION_TYPE_BUY else "SELL"
        open_time = datetime.fromtimestamp(p.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")

        result.append({
            "ticket": p.get("ticket"),
            "symbol": p.get("symbol"),
            "type": pos_type,
            "volume": round(float(p.get("volume", 0.0)), 2),
            "price_open": float(p.get("price_open", 0.0)),
            "price_current": float(p.get("price_current", 0.0)),
            "sl": float(p.get("sl", 0.0)),
            "tp": float(p.get("tp", 0.0)),
            "profit": round(float(p.get("profit", 0.0)), 2),
            "swap": float(p.get("swap", 0.0)),
            "comment": p.get("comment", ""),
            "open_time": open_time
        })

    return result


def create_position(symbol: str, order_type: str, lots: float, sl: float = 0.0, tp: float = 0.0, comment: str = "QuantAlgo"):
    """
    Opens a new market position (BUY / SELL).
    """
    if not symbol or not order_type or not lots:
        raise ValueError("Symbol, order_type (BUY/SELL), and lots are required")

    order_type_clean = order_type.strip().upper()
    if order_type_clean not in ["BUY", "SELL"]:
        raise ValueError("order_type must be either 'BUY' or 'SELL'")

    _ensure_mt5_connected()
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Symbol '{symbol}' not found in MetaTrader 5")

    # Enable in Market Watch if not visible
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Failed to enable symbol '{symbol}' in Market Watch")

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        raise RuntimeError(f"Failed to retrieve market price for symbol '{symbol}'")

    is_buy = order_type_clean == "BUY"
    price = tick.ask if is_buy else tick.bid
    mt5_order_type = mt5.ORDER_TYPE_BUY if is_buy else mt5.ORDER_TYPE_SELL

    # Resolve filling mode supported by broker
    filling_mode = symbol_info.filling_mode
    if filling_mode & 2:
        type_filling = mt5.ORDER_FILLING_IOC
    elif filling_mode & 1:
        type_filling = mt5.ORDER_FILLING_FOK
    else:
        type_filling = mt5.ORDER_FILLING_RETURN

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(lots),
        "type": mt5_order_type,
        "price": float(price),
        "deviation": 20,
        "magic": 202611,
        "comment": comment or "QuantAlgo Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }

    if sl > 0:
        request["sl"] = float(sl)
    if tp > 0:
        request["tp"] = float(tp)

    # Pre-check order
    check_res = mt5.order_check(request)
    if check_res is None or check_res.retcode != 0:
        err = check_res.comment if check_res else mt5.last_error()
        raise RuntimeError(f"Order check failed: {err}")

    # Dispatch order
    res = mt5.order_send(request)
    if res is None:
        raise RuntimeError(f"Order dispatch failed: {mt5.last_error()}")

    if res.retcode != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(f"Broker rejected trade: {res.comment} (code {res.retcode})")

    return {
        "ticket": res.order,
        "deal": res.deal,
        "symbol": symbol,
        "type": order_type_clean,
        "volume": res.volume,
        "price": res.price,
        "comment": res.comment,
        "status": "OPENED"
    }


def close_position_by_ticket(ticket: int):
    """
    Closes an active position by its ticket ID.
    """
    if not ticket:
        raise ValueError("Position ticket ID is required")

    _ensure_mt5_connected()
    positions = mt5.positions_get(ticket=int(ticket))
    if not positions:
        raise ValueError(f"Position #{ticket} not found or already closed in MT5")

    pos = positions[0]
    symbol = pos.symbol
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Symbol '{symbol}' not found in MT5")

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        raise RuntimeError(f"Failed to fetch market tick for {symbol}")

    is_buy = pos.type == mt5.POSITION_TYPE_BUY
    opposite_order_type = mt5.ORDER_TYPE_SELL if is_buy else mt5.ORDER_TYPE_BUY
    price = tick.bid if is_buy else tick.ask

    filling_mode = symbol_info.filling_mode
    if filling_mode & 2:
        type_filling = mt5.ORDER_FILLING_IOC
    elif filling_mode & 1:
        type_filling = mt5.ORDER_FILLING_FOK
    else:
        type_filling = mt5.ORDER_FILLING_RETURN

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": int(ticket),
        "symbol": symbol,
        "volume": float(pos.volume),
        "type": opposite_order_type,
        "price": float(price),
        "deviation": 20,
        "magic": 202611,
        "comment": "QuantAlgo Close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }

    check_res = mt5.order_check(request)
    if check_res is None or check_res.retcode != 0:
        err = check_res.comment if check_res else mt5.last_error()
        raise RuntimeError(f"Close check failed: {err}")

    res = mt5.order_send(request)
    if res is None:
        raise RuntimeError(f"Close order send failed: {mt5.last_error()}")

    if res.retcode != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(f"Broker rejected close: {res.comment} (code {res.retcode})")

    return {
        "ticket": ticket,
        "deal": res.deal,
        "symbol": symbol,
        "closed_volume": res.volume,
        "close_price": res.price,
        "comment": res.comment,
        "status": "CLOSED"
    }

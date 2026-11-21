from controllers.mt5_controller import (
    get_account_controller,
    get_positions_controller,
    create_position_controller,
    close_position_controller,
    get_symbols_controller
)


def register_routes(router):
    # MT5 Account Details & Available Symbols
    router["/api/mt5/account"] = get_account_controller
    router["/api/mt5/symbols"] = get_symbols_controller

    # MT5 Open/Running Positions
    router["/api/mt5/positions"] = get_positions_controller

    # MT5 Create & Close Position
    router["/api/mt5/position/create"] = create_position_controller
    router["/api/mt5/position/close"] = close_position_controller

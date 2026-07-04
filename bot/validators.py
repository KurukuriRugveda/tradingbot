import click

VALID_SIDES = {'BUY', 'SELL'}
VALID_TYPES = {'MARKET', 'LIMIT', 'STOP_MARKET', 'STOP_LIMIT'}

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """
    Validates user input data prior to hitting the API layer.
    Can be used by both CLI and UI.
    """
    symbol = symbol.strip().upper()
    side = side.strip().upper()
    order_type = order_type.strip().upper()

    if not symbol or len(symbol) < 5:
        raise ValueError("Symbol must be a valid pair string (e.g., BTCUSDT).")

    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}")

    if order_type not in VALID_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of {VALID_TYPES}")

    if quantity <= 0:
        raise ValueError("Quantity must be a positive number greater than 0.")

    if order_type == 'LIMIT':
        if price is None or price <= 0:
            raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")
            
    if order_type == 'STOP_MARKET':
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop Price is required and must be greater than 0 for STOP_MARKET orders.")

    if order_type == 'STOP_LIMIT':
        if price is None or price <= 0:
            raise ValueError("Limit Price is required and must be greater than 0 for STOP_LIMIT orders.")
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop/Trigger Price is required and must be greater than 0 for STOP_LIMIT orders.")

    return symbol, side, order_type, quantity, price, stop_price
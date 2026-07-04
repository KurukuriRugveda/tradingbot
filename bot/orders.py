from typing import Dict, Any
from bot.client import BinanceFuturesClient
from bot.logging_config import logger

class OrderManager:
    """Orchestrates order placement schemas and shapes clean operational context blocks."""
    
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None) -> Dict[str, Any]:
        """Constructs specific parameter payloads required for different order types."""
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = 'GTC'
        
        elif order_type == 'STOP_MARKET':
            params['stopPrice'] = stop_price
            
        elif order_type == 'STOP_LIMIT':
            # Binance Futures API recognizes Stop-Limit orders using the type specifier 'STOP'
            params['type'] = 'STOP'
            params['price'] = price
            params['stopPrice'] = stop_price
            params['timeInForce'] = 'GTC'

        logger.info(f"Initializing order dispatch context -> Pair: {symbol}, Side: {side}, Type: {order_type}, Qty: {quantity}")
        
        result = self.client.post_signed_request("/fapi/v1/order", params)
        return result
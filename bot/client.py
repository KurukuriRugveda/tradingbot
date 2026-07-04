import hmac
import hashlib
import time
import requests
from typing import Dict, Any
from bot.logging_config import logger

class BinanceFuturesClient:
    """Direct HTTP REST wrapper handling authentication and requests to Binance Futures Testnet."""
    
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            logger.error("API Credentials are missing or invalid inside environment variables.")
            raise ValueError("API Key and Secret must be configured.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _generate_signature(self, query_string: str) -> str:
        """Generates an HMAC-SHA256 signature for signed endpoints."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _get_server_time_offset(self) -> int:
        """Calculates difference between local clock and server clock to avoid timestamp errors."""
        try:
            url = f"{self.BASE_URL}/fapi/v1/time"
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            server_time = res.json()['serverTime']
            return server_time - int(time.time() * 1000)
        except Exception:
            return 0

    def post_signed_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a signed POST request safely with exception tracking."""
        url = f"{self.BASE_URL}{endpoint}"
        
        offset = self._get_server_time_offset()
        params['timestamp'] = int(time.time() * 1000) + offset
        params['recvWindow'] = 60000 

        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        signature = self._generate_signature(query_string)
        payload = f"{query_string}&signature={signature}"

        logger.debug(f"Sending POST Request to {url} with payload: {query_string}")

        try:
            response = self.session.post(url, data=payload, timeout=10)
            response_json = response.json()
            
            if response.status_code != 200:
                logger.error(f"API Error Response [HTTP {response.status_code}]: {response_json}")
                return {"success": False, "error": response_json.get("msg", "Unknown API error"), "code": response_json.get("code")}
            
            logger.info("API request completed successfully.")
            return {"success": True, "data": response_json}

        except requests.exceptions.Timeout:
            logger.error("Network connection timed out while reaching Binance Testnet.")
            return {"success": False, "error": "Network timeout. Check your internet connection."}
        except requests.exceptions.RequestException as e:
            logger.error(f"Network transport level crash: {str(e)}")
            return {"success": False, "error": f"Network transport error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected application failure: {str(e)}")
            return {"success": False, "error": f"Unexpected structural error: {str(e)}"}
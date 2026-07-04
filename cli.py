import os
import sys
import click
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.logging_config import logger
from bot.validators import validate_order_inputs
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager

load_dotenv()

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--symbol', '-s', type=str, help='Trading asset token pair.', prompt='Enter Symbol')
@click.option('--side', '-d', type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Execution side.', prompt='Enter Side (BUY/SELL)')
@click.option('--type', '-t', 'order_type', type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET', 'STOP_LIMIT'], case_sensitive=False), help='Order logic.', prompt='Enter Order Type')
@click.option('--quantity', '-q', type=float, help='Asset amount size.', prompt='Enter Quantity')
@click.option('--price', '-p', type=float, default=None, required=False, help='Required for LIMIT and STOP_LIMIT.')
@click.option('--stop-price', '-sp', type=float, default=None, required=False, help='Required for STOP_MARKET and STOP_LIMIT.')
def run_bot(symbol, side, order_type, quantity, price, stop_price):
    """ Simplified Binance Futures Testnet Trading Bot CLI."""
    click.secho("\n=== Binance Futures Testnet Order Processing ===", fg="cyan", bold=True)
    
    if order_type.upper() in ['LIMIT', 'STOP_LIMIT'] and not price:
        price = click.prompt("Enter execution limit price", type=float)
        
    if order_type.upper() in ['STOP_MARKET', 'STOP_LIMIT'] and not stop_price:
        stop_price = click.prompt("Enter trigger stop price", type=float)

    try:
        symbol, side, order_type, quantity, price, stop_price = validate_order_inputs(
            symbol, side, order_type, quantity, price, stop_price
        )
    except ValueError as e:
        click.secho(f" Input Validation Failed: {str(e)}", fg="red", bold=True)
        return

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        click.secho(" Execution Blocked: Missing API Keys in .env file.", fg="red", bold=True)
        return

    try:
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
        manager = OrderManager(client=client)
        
        click.echo("\n📡 Registering pipeline to Binance Testnet cloud...")
        response = manager.place_order(symbol, side, order_type, quantity, price, stop_price)
        
        if response.get("success"):
            data = response["data"]
            click.secho("\n✅ ORDER PLACED SUCCESSFULLY!", fg="green", bold=True)
            click.echo(f" 🆔 Order ID     : {data.get('orderId')}")
            click.echo(f" 📊 State Status : {data.get('status')}")
            click.echo(f" 📦 Executed Qty : {data.get('executedQty')}")
            click.echo(f" 🏷️ Avg Price    : {data.get('avgPrice', 'N/A') or data.get('price', 'N/A')}")
        else:
            click.secho("\n ORDER EXECUTION FAILED", fg="red", bold=True)
            click.echo(f" Reason / Context: {response.get('error')}")
            
    except Exception as general_err:
        click.secho(f"\n Pipeline Failure: {str(general_err)}", fg="red", bold=True)

if __name__ == "__main__":
    run_bot()
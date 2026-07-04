import os
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_order_inputs

# Load environment variables
load_dotenv()

class TradingBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binance Futures Testnet Bot")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # UI Styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        ttk.Label(root, text="⚡ Binance Futures Terminal", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        # Status Check
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        status_text = "🟢 API Keys Loaded" if self.api_key and self.api_secret else "🔴 Missing API Keys in .env"
        ttk.Label(root, text=status_text).pack(pady=5)

        # Input Frame
        frame = ttk.Frame(root, padding="20")
        frame.pack(fill="both", expand=True)

        # Form Fields
        ttk.Label(frame, text="Symbol (e.g., BTCUSDT):").grid(row=0, column=0, sticky="w", pady=5)
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        ttk.Entry(frame, textvariable=self.symbol_var).grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Order Type:").grid(row=1, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar(value="MARKET")
        type_dropdown = ttk.Combobox(frame, textvariable=self.type_var, values=["MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"], state="readonly")
        type_dropdown.grid(row=1, column=1, pady=5, sticky="ew")
        type_dropdown.bind("<<ComboboxSelected>>", self.toggle_fields)

        ttk.Label(frame, text="Side:").grid(row=2, column=0, sticky="w", pady=5)
        self.side_var = tk.StringVar(value="BUY")
        ttk.Combobox(frame, textvariable=self.side_var, values=["BUY", "SELL"], state="readonly").grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Quantity:").grid(row=3, column=0, sticky="w", pady=5)
        self.qty_var = tk.StringVar(value="0.01")
        ttk.Entry(frame, textvariable=self.qty_var).grid(row=3, column=1, pady=5, sticky="ew")

        self.price_label = ttk.Label(frame, text="Limit Price ($):")
        self.price_label.grid(row=4, column=0, sticky="w", pady=5)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(frame, textvariable=self.price_var, state="disabled")
        self.price_entry.grid(row=4, column=1, pady=5, sticky="ew")

        self.stop_label = ttk.Label(frame, text="Stop Price ($):")
        self.stop_label.grid(row=5, column=0, sticky="w", pady=5)
        self.stop_var = tk.StringVar()
        self.stop_entry = ttk.Entry(frame, textvariable=self.stop_var, state="disabled")
        self.stop_entry.grid(row=5, column=1, pady=5, sticky="ew")

        # Submit Button
        submit_btn = ttk.Button(root, text="🚀 Execute Order", command=self.execute_order)
        submit_btn.pack(pady=20, fill="x", padx=40)

    def toggle_fields(self, event=None):
        """Enable/Disable price fields dynamically based on order type."""
        order_type = self.type_var.get()
        
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            self.price_entry.config(state="normal")
        else:
            self.price_var.set("")
            self.price_entry.config(state="disabled")
            
        if order_type in ["STOP_MARKET", "STOP_LIMIT"]:
            self.stop_entry.config(state="normal")
        else:
            self.stop_var.set("")
            self.stop_entry.config(state="disabled")

    def execute_order(self):
        if not self.api_key or not self.api_secret:
            messagebox.showerror("Error", "Missing API Keys. Please configure your .env file.")
            return

        try:
            # Gather & parse inputs
            symbol = self.symbol_var.get()
            side = self.side_var.get()
            order_type = self.type_var.get()
            quantity = float(self.qty_var.get())
            price = float(self.price_var.get()) if self.price_var.get() else None
            stop_price = float(self.stop_var.get()) if self.stop_var.get() else None

            # Validate via our backend module
            v_sym, v_side, v_type, v_qty, v_price, v_stop = validate_order_inputs(
                symbol, side, order_type, quantity, price, stop_price
            )

            # Initialize Client & Dispatch
            client = BinanceFuturesClient(api_key=self.api_key, api_secret=self.api_secret)
            manager = OrderManager(client=client)
            response = manager.place_order(v_sym, v_side, v_type, v_qty, v_price, v_stop)

            # Handle Response
            if response.get("success"):
                data = response["data"]
                msg = f"✅ SUCCESS!\n\nOrder ID: {data.get('orderId')}\nStatus: {data.get('status')}\nExecuted Qty: {data.get('executedQty')}"
                messagebox.showinfo("Order Placed", msg)
            else:
                messagebox.showerror("Execution Failed", response.get("error"))

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("System Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotUI(root)
    root.mainloop()
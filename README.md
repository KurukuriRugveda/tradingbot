#  Binance Futures Trading Bot (Python CLI)

A production-ready **Python Command Line Interface (CLI)** application interacts with the **Binance USDT-M Futures Testnet API** to place **Market** and **Limit** orders securely.

The application follows clean software engineering practices by separating responsibilities into different modules, validating user inputs, maintaining detailed logs, handling exceptions gracefully, and keeping API credentials secure using environment variables.

---

##  Features

 Place **Market BUY** orders

 Place **Market SELL** orders

 Place **Limit BUY** orders

 Place **Limit SELL** orders

 Binance Futures Testnet Integration

 Secure API Key Management using `.env`

 Input Validation

 Comprehensive Logging

 Exception Handling

 Command Line Interface (CLI)


---

#  Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│   └── trading.log
│
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

#  Tech Stack

- Python 3.x
- Binance Futures Testnet API
- python-binance
- argparse
- logging
- python-dotenv
- requests

---

## Clone Repositor

```bash
git clone https://github.com/yourusername/binance-trading-bot.git
```

```bash
cd binance-trading-bot
```

---

## Create Virtual Environment (Recommended)

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Environment Variables

Create a `.env` file inside the project root.

```
API_KEY=YOUR_BINANCE_API_KEY
API_SECRET=YOUR_BINANCE_SECRET_KEY
```

Never share this file publicly.

---

#  Binance Testnet

Create a Binance Futures Testnet account.

Generate

- API Key
- Secret Key

Add them inside `.env`.

---

# Usage

## Market Order

```bash
python cli.py \
--symbol BTCUSDT \
--side BUY \
--type MARKET \
--quantity 0.001
```

Example

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## Limit Order

```bash
python cli.py \
--symbol BTCUSDT \
--side SELL \
--type LIMIT \
--quantity 0.001 \
--price 120000
```

Example

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

---

#  Example Output

```
=========================================
        ORDER SUMMARY
=========================================

Symbol      : BTCUSDT
Side        : BUY
Order Type  : MARKET
Quantity    : 0.001

=========================================

Sending Order...

=========================================

Order ID    : 843957382
Status      : FILLED
ExecutedQty : 0.001

Order placed successfully.

=========================================
```

---

#  Logging

Every API request and response is automatically recorded inside

```
logs/trading.log
```

Example

```
2026-07-04 11:32:18

INFO

Market BUY Order

Symbol : BTCUSDT

Quantity : 0.001

Status : FILLED

Order ID : 843957382
```

Errors are also logged for easier debugging.

---

#  Validation

The application validates:

- Trading Symbol
- Order Side
- Order Type
- Quantity
- Limit Price
- Empty Inputs
- Invalid Values

No API request is sent until all validations pass.

---

#  Exception Handling

The application handles

- Invalid API Keys
- Invalid Trading Symbols
- Invalid Quantity
- Network Errors
- Binance API Errors
- Unexpected Exceptions

The application exits gracefully with meaningful error messages instead of crashing.

---

#  Dependencies

```
python-binance
python-dotenv
requests
```

Install using

```bash
pip install -r requirements.txt
```

---

#  Testing:

The project had been tested using

- Binance Futures Testnet
- Python 3.x
- Windows 11

---










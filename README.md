# codetotrade-python-example
a complete example build a trading bot by using codetotrade.app

## Bot Algorithm
- Buy : RSI < 30
- Sell : RSI > 70
- Take profit : 5%
- Stop loss : 5%

## Requirement
- Python 3.10 -> 3.12
- ta-lib (https://pypi.org/project/TA-Lib/0.4.32/) 

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start

### Start the back test server
```bash
python ./src/back_test_main.py
```

### Start the binance server
```bash
python ./src/binance_server_main.py
```


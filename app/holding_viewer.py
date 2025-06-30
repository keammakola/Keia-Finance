import yfinance as yf
from tools import json_extractor

tickers = json_extractor("transactions","name")

for ticker in tickers:
    data = yf.Ticker(ticker)
    print(data.info['currentPrice'])


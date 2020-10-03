import finnhub #never reinvent the wheel,especially if it's official
import plotext.plot as plx
import time
import os

#I'm getting several parameters from environment variables
api_token = os.environ["FINNHUB_TOKEN_KEY"]#if this env var is unset will raise exception,as it should
cl = finnhub.Client(api_token)
#the rest have sensible defaults
currency = os.environ.get("FINNHUB_CURRENCY", "USD")
# USD should be multiplied by this number to be converted in currency
conversion_rate = cl.forex_rates(base="USD")["quote"][currency]

#several defaults
resolution=os.environ.get("FINNHUB_RESOLUTION","D")
to = int(os.environ.get("FINNHUB_TO",time.time()))#up to now by default
_from = int(os.environ.get("FINNHUB_FROM", to - (8600 * 30 * 12)))  #data from the previous year by default

def print_stock(symbol="AAPL"):
  "Print all the required data about the given stock"
  print("Stock symbol:", symbol)
  try:
    profile = cl.company_profile2(symbol=symbol)
    #Pretty printing the data retrived by the API
    for k in iter(profile):
      print(k,":",profile[k])
    print("Current price:", cl.quote(symbol)["c"] * conversion_rate)
    candle=cl.stock_candles(symbol, resolution, _from, to)
    x = candle["t"]#representing the timestamps
    #converting the values from USD
    y = [c*conversion_rate for c in candle["c"]]
    plx.scatter(x, y)
    plx.show()
    print()
  except:pass#sometimes company_profile2 return something weird like an {} for AACQW 
  
def print_forex(symbol="OANDA:EUR_USD"):
  "Print all required data about the given forex"
  print("Forex symbol:",symbol)
  candle=cl.forex_candles(symbol, resolution, _from, to)
  x = candle["t"]
  y = candle["c"]
  plx.scatter(x, y)
  plx.show()
  print()
  
def print_exch(from_curr="EUR", to_curr="USD", forex="OANDA"):
  "A simple wrapper around print_forex with sensible defaults"
  print_forex("{}:{}_{}".format(forex,from_curr,to_curr))